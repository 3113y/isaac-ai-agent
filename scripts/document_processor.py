#!/usr/bin/env python3
"""
Isaac API 文档处理器 - 使用 DeepSeek API 进行文档清洗
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys

try:
    import anthropic
except ImportError:
    print("❌ 缺少依赖：pip install anthropic pyyaml loguru")
    sys.exit(1)

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class APIDocumentProcessor:
    """Isaac API 文档处理器 - 基于 DeepSeek (prompt 缓存优化版)"""

    # 统一的 System Prompt，所有调用共用以提升缓存命中率
    SYSTEM_PROMPT = (
        "You are an API documentation analysis assistant for The Binding of Isaac: Repentance. "
        "You analyze class documentation and output strictly valid JSON with enhancement information "
        "including summaries, use cases, and related methods."
    )

    # 增强请求的固定前缀（所有类共用 — DeepSeek 上下文缓存的命中区域）
    ENHANCEMENT_FIXED_PREFIX = """你是《以撒的结合》API 文档分析助手，请严格输出 JSON。

规则：
1. 当前请求只对应一个类/对象，不要跨类推断。
2. 同一个类的全部方法在同一上下文中统一分析，避免重复和错乱。
3. 先输出类级总结，再输出每个方法的独立总结。
4. method_id 必须与输入一致，不可新增、不可遗漏。
5. 输出必须是 JSON 对象，禁止输出 markdown 代码块和额外解释。

返回格式：
{
  "class_enhancement": {
    "summary": "类整体作用总结",
    "use_cases": ["用途1", "用途2"],
    "key_methods": ["关键方法1", "关键方法2"]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "该方法的独立总结",
      "use_cases": ["该方法用途1", "该方法用途2"],
      "key_methods": ["相关方法或调用点"]
    }
  ]
}

额外要求：
- class_enhancement.key_methods 只能引用当前类中的方法名。
- 每个 method_enhancement.summary 必须针对对应 method_id，禁止复用同一段文本。
- 每个 method_enhancement.key_methods 的第一个元素必须是该 method_id 对应的方法名。
- use_cases 和 key_methods 每项尽量简洁，最多 5 项。"""

    def __init__(self, docs_dir: str = "docs", output_dir: str = "processed_docs"):
        self.docs_dir = Path(docs_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 优先使用 Anthropic 标准变量，并兼容历史 DEEPSEEK_* 变量。
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("❌ 未设置 ANTHROPIC_API_KEY (或兼容的 DEEPSEEK_API_KEY) 环境变量")

        base_url = os.getenv("ANTHROPIC_BASE_URL") or os.getenv("ANTHROPIC_API_BASE")
        if not base_url:
            base_url = "https://api.deepseek.com/anthropic"

        self.model = os.getenv("DEEPSEEK_ANTHROPIC_MODEL", "deepseek-v4-pro")
        self.client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
        logger.info(f"✅ DeepSeek 客户端已初始化 (model={self.model}, base_url={base_url})")

        try:
            self.max_doc_context_chars = max(4000, int(os.getenv("DEEPSEEK_DOC_CONTEXT_CHARS", "16000")))
        except ValueError:
            self.max_doc_context_chars = 16000

        try:
            self.max_response_tokens = max(1200, int(os.getenv("DEEPSEEK_MAX_RESPONSE_TOKENS", "6000")))
        except ValueError:
            self.max_response_tokens = 2600

        self.save_context_docs = os.getenv("SAVE_DEEPSEEK_CONTEXT", "1").strip().lower() not in {
            "0", "false", "no"
        }

        self.debug_dir = self.output_dir / "debug"
        self.context_dir = self.debug_dir / "deepseek_contexts"
        self.failed_response_dir = self.debug_dir / "failed_responses"
        self.debug_dir.mkdir(exist_ok=True)
        self.failed_response_dir.mkdir(exist_ok=True)
        if self.save_context_docs:
            self.context_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "errors": 0,
            "total_methods": 0
        }

    @staticmethod
    def _normalize_list(values: Any, fallback: List[str]) -> List[str]:
        if not isinstance(values, list):
            return fallback

        cleaned = [str(v).strip() for v in values if str(v).strip()]
        if not cleaned:
            return fallback
        return cleaned[:5]

    @staticmethod
    def _dedupe_keep_order(values: List[str]) -> List[str]:
        seen = set()
        result = []
        for value in values:
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    def _normalize_class_key_methods(
        self,
        key_methods: List[str],
        valid_method_names: List[str],
        fallback_key_methods: List[str],
    ) -> List[str]:
        valid_set = {name for name in valid_method_names if name}
        filtered = [name for name in key_methods if name in valid_set]
        if not filtered:
            filtered = [name for name in fallback_key_methods if name in valid_set]
        if not filtered:
            filtered = valid_method_names[:5]
        return self._dedupe_keep_order(filtered)[:5]

    def _normalize_method_key_methods(self, key_methods: List[str], method_name: str) -> List[str]:
        normalized = [method_name] if method_name else []
        normalized.extend(key_methods)
        normalized = self._dedupe_keep_order([name for name in normalized if name])
        if not normalized:
            return ["Unknown"]
        return normalized[:5]

    def _normalize_enhancement_block(
        self,
        data: Any,
        fallback_summary: str,
        fallback_use_cases: List[str],
        fallback_key_methods: List[str],
    ) -> Dict[str, Any]:
        if not isinstance(data, dict):
            data = {}

        summary = data.get("summary", "")
        if not isinstance(summary, str) or not summary.strip():
            summary = fallback_summary

        return {
            "summary": summary.strip(),
            "use_cases": self._normalize_list(data.get("use_cases"), fallback_use_cases),
            "key_methods": self._normalize_list(data.get("key_methods"), fallback_key_methods),
        }

    def _build_class_fallback_enhancement(self, api_info: Dict[str, Any]) -> Dict[str, Any]:
        method_names = [m.get("name", "") for m in api_info.get("methods", []) if m.get("name")]
        key_methods = method_names[:5]
        use_cases = [
            f"在 Mod 脚本中调用 {api_info['title']} 的能力",
            f"结合 {api_info['title']} 的关键方法实现玩法逻辑",
        ]

        return {
            "summary": f"{api_info['title']} 的 API 文档摘要。",
            "use_cases": use_cases,
            "key_methods": key_methods,
        }

    def _build_method_fallback_enhancement(self, method: Dict[str, Any]) -> Dict[str, Any]:
        description = (method.get("description") or "").strip()
        summary = description if description else f"{method.get('name', 'Unknown')} 方法说明。"

        return {
            "summary": summary,
            "use_cases": [f"调用 {method.get('name', 'Unknown')} 完成对应 API 操作"],
            "key_methods": [method.get("name", "Unknown")],
        }

    @staticmethod
    def _strip_code_fences(raw_text: str) -> str:
        text = raw_text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _extract_json_text(raw_text: str) -> str:
        text = APIDocumentProcessor._strip_code_fences(raw_text)
        start = text.find("{")
        if start == -1:
            raise ValueError("响应中未找到有效 JSON")

        depth = 0
        in_string = False
        escaped = False
        for idx in range(start, len(text)):
            ch = text[idx]

            if escaped:
                escaped = False
                continue

            if ch == "\\":
                escaped = True
                continue

            if ch == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:idx + 1]

        raise ValueError("响应中的 JSON 不完整，可能被截断")

    @staticmethod
    def _fix_common_json_issues(json_text: str) -> str:
        fixed = json_text
        fixed = fixed.replace("“", '"').replace("”", '"')
        fixed = fixed.replace("‘", "'").replace("’", "'")
        fixed = re.sub(r",\s*([}\]])", r"\1", fixed)
        return fixed

    @staticmethod
    def _safe_name(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_") or "unknown"

    def _save_context_doc(
        self,
        class_title: str,
        stage: str,
        attempt: int,
        prompt: str,
        response: str,
        max_tokens: int,
        temperature: float,
    ):
        if not self.save_context_docs:
            return

        self.context_dir.mkdir(exist_ok=True)
        safe_title = self._safe_name(class_title)
        safe_stage = self._safe_name(stage)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = self.context_dir / f"{safe_title}__{safe_stage}__a{attempt:02d}__{timestamp}.md"

        content = (
            f"# DeepSeek Context\n\n"
            f"- class: {class_title}\n"
            f"- stage: {stage}\n"
            f"- attempt: {attempt}\n"
            f"- model: {self.model}\n"
            f"- max_tokens: {max_tokens}\n"
            f"- temperature: {temperature}\n"
            f"- timestamp: {datetime.now().isoformat()}\n\n"
            f"## Prompt\n\n"
            f"```text\n{prompt}\n```\n\n"
            f"## Response\n\n"
            f"```text\n{response}\n```\n"
        )
        file_path.write_text(content, encoding="utf-8")

    def _call_deepseek(
        self,
        *,
        prompt: str,
        system: str,
        max_tokens: int,
        temperature: float,
        class_title: str,
        stage: str,
        attempt: int,
        fixed_prefix: str = "",
        empty_retries: int = 2,
    ) -> str:
        # 合并 fixed_prefix + prompt（缓存优化靠固定前缀在前面的结构，不依赖 cache_control）
        full_prompt = (fixed_prefix + prompt) if fixed_prefix else prompt

        last_response_text = ""
        for empty_attempt in range(empty_retries + 1):
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt,
                    }
                ],
            )

            response_text = "\n".join(
                block.text for block in message.content if getattr(block, "type", None) == "text"
            )

            if response_text:
                self._save_context_doc(
                    class_title=class_title,
                    stage=stage,
                    attempt=attempt,
                    prompt=full_prompt,
                    response=response_text,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response_text

            # 空响应：等待后重试
            last_response_text = response_text
            if empty_attempt < empty_retries:
                import time
                wait = (empty_attempt + 1) * 3
                logger.warning(
                    f"⚠️  空响应 {class_title} (第{empty_attempt+1}次), {wait}s 后重试..."
                )
                time.sleep(wait)

        # 保存最后失败的上下文
        self._save_context_doc(
            class_title=class_title,
            stage=stage,
            attempt=attempt,
            prompt=full_prompt,
            response="",
            max_tokens=max_tokens,
            temperature=temperature,
        )
        raise ValueError("DeepSeek 返回内容为空（重试{}次仍为空）".format(empty_retries))

    def _save_failed_response(self, class_title: str, raw_text: str):
        self.failed_response_dir.mkdir(exist_ok=True)

        safe_title = self._safe_name(class_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = self.failed_response_dir / f"{safe_title}__{timestamp}.txt"
        file_path.write_text(raw_text, encoding="utf-8")

    def _repair_json_with_deepseek(self, broken_json_text: str, class_title: str, attempt: int = 1) -> str:
        repair_fixed = (
            "请把下面这段损坏的 JSON 文本修复为严格合法的 JSON。\n\n"
            "要求：\n"
            "1. 只输出 JSON 对象，不要任何解释。\n"
            "2. 尽量保留原字段和语义，不要新增无关字段。\n"
            "3. 顶层结构应为 {\"class_enhancement\": ..., \"method_enhancements\": ...}。\n"
        )
        repair_variable = f"类名：{class_title}\n\n损坏的 JSON：\n{broken_json_text}"

        repair_text = self._call_deepseek(
            prompt=repair_variable,
            fixed_prefix=repair_fixed,
            system=self.SYSTEM_PROMPT,
            max_tokens=max(self.max_response_tokens, 3200),
            temperature=0,
            class_title=class_title,
            stage="repair_json",
            attempt=attempt,
        )
        return repair_text

    def _parse_ai_json_response(self, response_text: str, class_title: str) -> Dict[str, Any]:
        extracted = ""
        try:
            extracted = self._extract_json_text(response_text)
        except ValueError as extract_error:
            logger.warning(f"⚠️  JSON 提取失败 {class_title}: {extract_error}; 尝试修复")
            raw = self._strip_code_fences(response_text)
            start = raw.find("{")
            candidate = raw[start:] if start != -1 else raw
            candidate = self._fix_common_json_issues(candidate)

            try:
                llm_repaired = self._repair_json_with_deepseek(candidate, class_title, attempt=1)
                repaired_extracted = self._extract_json_text(llm_repaired)
                return json.loads(repaired_extracted)
            except Exception as repair_error:
                self._save_failed_response(class_title, response_text)
                raise ValueError(f"{extract_error}; 自动修复失败: {repair_error}") from repair_error

        try:
            return json.loads(extracted)
        except json.JSONDecodeError as first_error:
            repaired_text = self._fix_common_json_issues(extracted)
            try:
                return json.loads(repaired_text)
            except json.JSONDecodeError:
                logger.warning(f"⚠️  JSON 初次解析失败 {class_title}: {first_error}; 尝试模型修复")

            try:
                llm_repaired = self._repair_json_with_deepseek(repaired_text, class_title, attempt=2)
                repaired_extracted = self._extract_json_text(llm_repaired)
                return json.loads(repaired_extracted)
            except Exception as repair_error:
                self._save_failed_response(class_title, response_text)
                raise ValueError(f"JSON 解析失败且修复失败: {repair_error}") from repair_error

    def _build_enhancement_prompt(
        self,
        api_info: Dict[str, Any],
        doc_context_chars: Optional[int] = None,
        compact: bool = False,
    ) -> tuple:
        methods_payload = [
            {
                "method_id": method.get("id"),
                "name": method.get("name"),
                "signature": method.get("signature"),
                "description": method.get("description"),
            }
            for method in api_info.get("methods", [])
        ]

        max_context = self.max_doc_context_chars if doc_context_chars is None else max(2000, doc_context_chars)
        raw_doc = api_info.get("raw_doc", "")
        if len(raw_doc) > max_context:
            raw_doc = (
                raw_doc[: max_context]
                + "\n\n[TRUNCATED: 原文过长，已截断以适配上下文窗口]"
            )

        methods_json = json.dumps(methods_payload, ensure_ascii=False, indent=2)

        compact_note = (
            "\n压缩输出：summary 尽量控制在 60 字内，use_cases 不超过 2 项，key_methods 不超过 3 项。"
            if compact
            else ""
        )

        # 固定前缀：所有类共用，可被 DeepSeek 输入缓存 100% 命中
        fixed_prefix = self.ENHANCEMENT_FIXED_PREFIX

        # 可变后缀：每类不同（compact 提示也放这里，确保固定前缀最大复用）
        variable_suffix = (
            compact_note
            + f"\n\n类名：{api_info['title']}\n\n"
            + f"原始 md 文档（该类完整文档，可能已截断）：\n{raw_doc}\n\n"
            + f"方法列表（JSON）：\n{methods_json}\n"
        )

        return fixed_prefix, variable_suffix
    
    # CSS badge class → compatible DLC versions
    BADGE_TO_VERSIONS = {
        "alldlc": ["AB+", "REP", "REP+"],
        "reporplus": ["REP", "REP+"],
        "abrep": ["AB+", "REP"],
        "repplus": ["REP+"],
        "rep": ["REP"],
        "abp": ["AB+"],
    }
    MODIFIER_CLASSES = {"static", "const"}

    @classmethod
    def _parse_badge_line(cls, between_text: str) -> tuple:
        """Extract DLC versions and modifiers from badge classes between ### and ####."""
        badge_match = re.search(r"\[ ?\]\(#\)\{\: ([^}]*?) \}", between_text)
        if not badge_match:
            return [], []

        badge_str = badge_match.group(1).strip()
        all_known = set(cls.BADGE_TO_VERSIONS.keys()) | cls.MODIFIER_CLASSES

        versions = []
        modifiers = []
        for token in badge_str.split():
            token = token.strip().lstrip(".")
            if token in cls.BADGE_TO_VERSIONS:
                versions.extend(cls.BADGE_TO_VERSIONS[token])
            elif token in cls.MODIFIER_CLASSES:
                modifiers.append(token)

        # Deduplicate while preserving order
        seen = set()
        unique_versions = []
        for v in versions:
            if v not in seen:
                seen.add(v)
                unique_versions.append(v)

        return unique_versions, modifiers

    def extract_class_info(self, content: str, filename: str) -> dict:
        """从文档提取类/函数信息（含 DLC 版本标签）"""

        # 移除 frontmatter
        content_clean = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)

        # 提取标题
        title_match = re.search(r'^# .*?"([^"]+)"', content_clean, re.MULTILINE)
        title = title_match.group(1) if title_match else filename.replace('.md', '')

        # 提取所有函数/方法
        methods = []
        method_pattern = r'### ([^\n]+)\n.*?\n#### (.*?)\n(.*?)(?=^###|$)'
        matches = re.finditer(method_pattern, content_clean, re.MULTILINE | re.DOTALL)

        for index, match in enumerate(matches, start=1):
            method_name = match.group(1).strip()
            signature = match.group(2).strip()
            description = match.group(3).strip()

            # 清洗方法名
            method_name = re.sub(r'·', '', method_name)
            method_name = re.sub(r'\s*\(\)\s*.*', '', method_name)
            method_name = re.sub(r'\s*\{:\s*.*\}\s*$', '', method_name)
            method_name = method_name.strip()

            # 提取 DLC 版本标签和修饰符
            versions, modifiers = self._parse_badge_line(match.group(0))

            methods.append({
                "id": f"m{index:03d}",
                "name": method_name,
                "signature": signature,
                "description": description[:500],
                "versions": versions,
                "modifiers": modifiers,
            })

        return {
            "filename": filename,
            "title": title,
            "methods_count": len(methods),
            "methods": methods,
            "raw_doc": content_clean.strip(),
        }
    
    def _compute_max_tokens(self, method_count: int, compact: bool) -> int:
        """根据方法数量动态计算 max_tokens：每个方法约需 200 tokens 的 JSON 输出"""
        base = 1200  # class_enhancement 的开销
        per_method = 150 if compact else 250
        needed = base + method_count * per_method
        return max(self.max_response_tokens, min(needed, 16000))

    def enhance_with_deepseek(self, api_info: dict) -> dict:
        """使用 DeepSeek 增强 API 信息（支持大类别自动分批）"""
        method_count = len(api_info.get("methods", []))
        class_fallback = self._build_class_fallback_enhancement(api_info)
        method_fallbacks = {
            method["id"]: self._build_method_fallback_enhancement(method)
            for method in api_info.get("methods", [])
        }

        # 先写入兜底
        api_info["enhancement"] = class_fallback
        api_info["method_enhancements"] = method_fallbacks

        # 大类别（>50 方法）分批处理
        BATCH_THRESHOLD = 50
        if method_count > BATCH_THRESHOLD:
            return self._enhance_with_batching(api_info, class_fallback, method_fallbacks)

        try:
            ai_data = None
            last_error = None

            attempt_settings = [
                {
                    "attempt": 1,
                    "doc_chars": self.max_doc_context_chars,
                    "max_tokens": self._compute_max_tokens(method_count, compact=False),
                    "compact": False,
                    "temperature": 0.2,
                },
                {
                    "attempt": 2,
                    "doc_chars": max(4000, self.max_doc_context_chars // 2),
                    "max_tokens": self._compute_max_tokens(method_count, compact=True),
                    "compact": True,
                    "temperature": 0,
                },
            ]

            for setting in attempt_settings:
                fixed_prefix, variable_suffix = self._build_enhancement_prompt(
                    api_info,
                    doc_context_chars=setting["doc_chars"],
                    compact=setting["compact"],
                )

                response_text = self._call_deepseek(
                    prompt=variable_suffix,
                    fixed_prefix=fixed_prefix,
                    system=self.SYSTEM_PROMPT,
                    max_tokens=setting["max_tokens"],
                    temperature=setting["temperature"],
                    class_title=api_info["title"],
                    stage="enhancement",
                    attempt=setting["attempt"],
                )

                try:
                    ai_data = self._parse_ai_json_response(response_text, api_info["title"])
                    break
                except Exception as parse_error:
                    last_error = parse_error
                    logger.warning(
                        f"⚠️  解析失败 {api_info['title']} 第{setting['attempt']}次: {parse_error}"
                    )

            if ai_data is None:
                raise ValueError(f"增强响应解析失败: {last_error}")

        except Exception as e:
            logger.warning(f"⚠️  增强失败 {api_info['title']}: {e}")
            return api_info

        return self._apply_enhancement_data(
            api_info, ai_data, class_fallback, method_fallbacks
        )

    def _apply_enhancement_data(
        self,
        api_info: dict,
        ai_data: Dict[str, Any],
        class_fallback: Dict[str, Any],
        method_fallbacks: Dict[str, Dict[str, Any]],
    ) -> dict:
        """将 AI 增强数据归一化并写回 api_info"""
        class_raw = ai_data.get("class_enhancement", ai_data)
        class_enhancement = self._normalize_enhancement_block(
            class_raw,
            class_fallback["summary"],
            class_fallback["use_cases"],
            class_fallback["key_methods"],
        )
        valid_method_names = [m.get("name", "") for m in api_info.get("methods", []) if m.get("name")]
        class_enhancement["key_methods"] = self._normalize_class_key_methods(
            class_enhancement.get("key_methods", []),
            valid_method_names,
            class_fallback["key_methods"],
        )

        method_raw_list = ai_data.get("method_enhancements", [])
        method_enhancements: Dict[str, Dict[str, Any]] = {}

        if isinstance(method_raw_list, dict):
            method_raw_list = [
                {"method_id": method_id, **payload}
                for method_id, payload in method_raw_list.items()
                if isinstance(payload, dict)
            ]

        if isinstance(method_raw_list, list):
            for method_item in method_raw_list:
                if not isinstance(method_item, dict):
                    continue
                method_id = str(method_item.get("method_id", "")).strip()
                if not method_id:
                    continue
                method_enhancements[method_id] = method_item

        normalized_method_enhancements = {}
        for method in api_info.get("methods", []):
            method_id = method.get("id")
            fallback = method_fallbacks.get(method_id, self._build_method_fallback_enhancement(method))
            method_block = self._normalize_enhancement_block(
                method_enhancements.get(method_id),
                fallback["summary"],
                fallback["use_cases"],
                fallback["key_methods"],
            )
            method_block["key_methods"] = self._normalize_method_key_methods(
                method_block.get("key_methods", []),
                method.get("name", "Unknown"),
            )
            normalized_method_enhancements[method_id] = method_block

        api_info["enhancement"] = class_enhancement
        api_info["method_enhancements"] = normalized_method_enhancements
        logger.info(f"✅ 增强完成: {api_info['title']} (方法增强: {len(normalized_method_enhancements)})")
        return api_info

    def _enhance_with_batching(
        self,
        api_info: dict,
        class_fallback: Dict[str, Any],
        method_fallbacks: Dict[str, Dict[str, Any]],
    ) -> dict:
        """大类别（>50 方法）分批处理，每批最多 40 个方法"""
        methods = api_info.get("methods", [])
        batch_size = 40
        all_method_enhancements: Dict[str, Dict[str, Any]] = {}
        class_enhancement = class_fallback

        for batch_idx in range(0, len(methods), batch_size):
            batch_methods = methods[batch_idx:batch_idx + batch_size]
            batch_api_info = {
                **api_info,
                "methods": batch_methods,
            }
            batch_fallbacks = {
                m["id"]: method_fallbacks.get(m["id"], self._build_method_fallback_enhancement(m))
                for m in batch_methods
            }

            ai_data = None
            last_error = None
            method_count = len(batch_methods)

            for attempt in range(1, 3):
                compact = attempt == 2
                fixed_prefix, variable_suffix = self._build_enhancement_prompt(
                    batch_api_info,
                    doc_context_chars=self.max_doc_context_chars if attempt == 1 else max(4000, self.max_doc_context_chars // 2),
                    compact=compact,
                )

                try:
                    response_text = self._call_deepseek(
                        prompt=variable_suffix,
                        fixed_prefix=fixed_prefix,
                        system=self.SYSTEM_PROMPT,
                        max_tokens=self._compute_max_tokens(method_count, compact),
                        temperature=0.2 if attempt == 1 else 0,
                        class_title=f"{api_info['title']}[batch{batch_idx//batch_size + 1}]",
                        stage="enhancement",
                        attempt=attempt,
                    )
                    ai_data = self._parse_ai_json_response(response_text, api_info["title"])
                    break
                except Exception as parse_error:
                    last_error = parse_error
                    logger.warning(
                        f"⚠️  分批解析失败 {api_info['title']} 批次{batch_idx//batch_size + 1} 第{attempt}次: {parse_error}"
                    )

            if ai_data is not None:
                # 提取本批次的 class_enhancement（只取第一批的）
                if batch_idx == 0:
                    class_raw = ai_data.get("class_enhancement", ai_data)
                    class_enhancement = self._normalize_enhancement_block(
                        class_raw,
                        class_fallback["summary"],
                        class_fallback["use_cases"],
                        class_fallback["key_methods"],
                    )
                    valid_method_names = [m.get("name", "") for m in methods if m.get("name")]
                    class_enhancement["key_methods"] = self._normalize_class_key_methods(
                        class_enhancement.get("key_methods", []),
                        valid_method_names,
                        class_fallback["key_methods"],
                    )

                # 提取本批次的方法增强
                method_raw = ai_data.get("method_enhancements", [])
                if isinstance(method_raw, dict):
                    method_raw = [
                        {"method_id": k, **v}
                        for k, v in method_raw.items()
                        if isinstance(v, dict)
                    ]
                if isinstance(method_raw, list):
                    for item in method_raw:
                        if isinstance(item, dict) and item.get("method_id"):
                            all_method_enhancements[str(item["method_id"]).strip()] = item
            else:
                logger.warning(
                    f"⚠️  分批失败 {api_info['title']} 批次{batch_idx//batch_size + 1}: "
                    f"{last_error}，使用 fallback"
                )

        # 归一化所有方法增强
        normalized = {}
        for method in methods:
            method_id = method.get("id")
            fallback = method_fallbacks.get(method_id, self._build_method_fallback_enhancement(method))
            method_block = self._normalize_enhancement_block(
                all_method_enhancements.get(method_id),
                fallback["summary"],
                fallback["use_cases"],
                fallback["key_methods"],
            )
            method_block["key_methods"] = self._normalize_method_key_methods(
                method_block.get("key_methods", []),
                method.get("name", "Unknown"),
            )
            normalized[method_id] = method_block

        api_info["enhancement"] = class_enhancement
        api_info["method_enhancements"] = normalized
        logger.info(f"✅ 分批增强完成: {api_info['title']} (方法: {len(normalized)}, 批次: {(len(methods) + batch_size - 1) // batch_size})")
        return api_info
    
    def process_file(self, filepath: Path) -> Optional[dict]:
        """处理单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            api_info = self.extract_class_info(content, filepath.name)
            api_info = self.enhance_with_deepseek(api_info)
            api_info.pop("raw_doc", None)
            
            self.stats["processed_files"] += 1
            self.stats["total_methods"] += api_info["methods_count"]
            return api_info
            
        except Exception as e:
            logger.error(f"❌ 处理失败 {filepath.name}: {e}")
            self.stats["errors"] += 1
            return None
    
    def process_all(self):
        """处理所有文档"""
        
        print("\n" + "="*60)
        print("🚀 Isaac API 文档处理器 - DeepSeek")
        print("="*60)
        
        # 找所有 .md 文件
        md_files = sorted([
            f for f in self.docs_dir.glob("*.md")
            if f.name not in ["index.md", "PLACEHOLDER.md", "tags.md"]
            and not f.name.startswith("_")
        ])
        
        self.stats["total_files"] = len(md_files)
        print(f"\n📋 发现 {len(md_files)} 个文件\n")
        
        processed_data = []
        
        for i, filepath in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] {filepath.name}...", end=" ", flush=True)
            api_info = self.process_file(filepath)
            
            if api_info:
                processed_data.append(api_info)
                print(f"✅")
            else:
                print("❌")
        
        # 生成 RAG 格式
        rag_data = self._generate_rag_format(processed_data)
        
        # 保存结果
        self._save_results(processed_data, rag_data)
        
        # 显示统计
        print("\n" + "="*60)
        print("✅ 处理完成")
        print(f"   总文件: {self.stats['total_files']}")
        print(f"   成功: {self.stats['processed_files']}")
        print(f"   失败: {self.stats['errors']}")
        print(f"   总方法: {self.stats['total_methods']}")
        print("="*60 + "\n")
    
    def _generate_rag_format(self, data: list) -> list:
        """生成 RAG 格式数据"""
        rag_data = []
        for api in data:
            class_enhancement = api.get("enhancement", {})
            method_enhancements = api.get("method_enhancements", {})
            for method in api.get("methods", []):
                method_id = method.get("id")
                method_enhancement = method_enhancements.get(method_id, class_enhancement)
                rag_data.append({
                    "class": api["title"],
                    "method_id": method_id,
                    "function": method["name"],
                    "signature": method["signature"],
                    "description": method["description"],
                    "versions": method.get("versions", []),
                    "modifiers": method.get("modifiers", []),
                    "libraries": [],  # reserved for Curlib/RGON
                    "enhancement": method_enhancement,
                    "class_enhancement": class_enhancement,
                })
        return rag_data
    
    def _save_results(self, processed_data: list, rag_data: list):
        """保存处理结果"""

        self._organize_output_docs()
        
        # 保存原始数据
        output_path = self.output_dir / "processed_apis.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 已保存: {output_path}")
        
        # 保存 RAG 知识库
        output_path = self.output_dir / "rag_knowledge_base.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rag_data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 已保存: {output_path}")
        
        # 保存统计报告
        report = {
            "total_classes": len(processed_data),
            "total_methods": sum(d["methods_count"] for d in processed_data),
            "total_api_entries": len(rag_data),
            "stats": self.stats
        }
        output_path = self.output_dir / "report.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 已保存: {output_path}")

    def _organize_output_docs(self):
        """梳理输出目录中的调试文档与说明文件"""
        self.debug_dir.mkdir(exist_ok=True)
        self.failed_response_dir.mkdir(exist_ok=True)
        if self.save_context_docs:
            self.context_dir.mkdir(exist_ok=True)

        for preview_file in self.output_dir.glob("*_preview.json"):
            target = self.debug_dir / preview_file.name
            if target.exists():
                target.unlink()
            preview_file.replace(target)

        legacy_failed_dir = self.output_dir / "_failed_responses"
        if legacy_failed_dir.exists() and legacy_failed_dir.is_dir():
            for old_file in legacy_failed_dir.glob("*"):
                if old_file.is_file():
                    target = self.failed_response_dir / old_file.name
                    if target.exists():
                        target.unlink()
                    old_file.replace(target)
            legacy_failed_dir.rmdir()

        readme_path = self.output_dir / "README.md"
        readme_text = (
            "# Processed Docs\n\n"
            "- processed_apis.json: 类级与方法级提取结果。\n"
            "- rag_knowledge_base.json: RAG 使用的扁平化知识库。\n"
            "- report.json: 本次处理统计。\n"
            "- debug/deepseek_contexts/: 每次与 DeepSeek 的上下文请求与响应（一个上下文一个文档）。\n"
            "- debug/failed_responses/: 解析失败时保存的原始响应。\n"
        )
        readme_path.write_text(readme_text, encoding="utf-8")


def main():
    """主函数"""
    try:
        processor = APIDocumentProcessor(docs_dir="docs", output_dir="processed_docs")
        processor.process_all()
        
        print("💡 结果已保存到 processed_docs/ 目录:")
        print("   - processed_apis.json (原始提取数据)")
        print("   - rag_knowledge_base.json (RAG 系统数据)")
        print("   - report.json (统计报告)")
        print("   - debug/deepseek_contexts/ (DeepSeek 交互上下文，每次请求一个文档)")
        print("   - debug/failed_responses/ (解析失败原始响应)")
        
    except ValueError as e:
        print(f"\n{e}")
        print("\n🔑 设置环境变量:")
        print("   PowerShell: $env:ANTHROPIC_API_KEY = 'sk-...'")
        print("   PowerShell: $env:ANTHROPIC_BASE_URL = 'https://api.deepseek.com/anthropic'")
        print("   (兼容)     $env:DEEPSEEK_API_KEY = 'sk-...'")
        print("   或在 .env 文件中设置")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="<level>{level: <8}</level> | {message}",
        level="INFO"
    )
    
    main()
