#!/usr/bin/env python3
"""Retry failed classes from previous document processing run"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.document_processor import APIDocumentProcessor
from pathlib import Path


def main():
    # 读取之前的处理结果，找出 fallback 类
    processed_path = Path("processed_docs/processed_apis.json")
    with open(processed_path, "r", encoding="utf-8") as f:
        processed_data = json.load(f)

    failed = []
    for api in processed_data:
        enh = api.get("enhancement", {})
        summary = enh.get("summary", "")
        if summary.endswith("的 API 文档摘要。"):
            failed.append(api)

    print(f"找到 {len(failed)} 个失败类需要重试:\n")
    for api in failed:
        print(f"  - {api['title']} ({api['methods_count']} methods)")

    if not failed:
        print("没有需要重试的类")
        return

    # 初始化处理器
    proc = APIDocumentProcessor(docs_dir="docs", output_dir="processed_docs")

    # 逐个重试
    success = 0
    for api_info in failed:
        title = api_info["title"]
        filename = api_info.get("filename", f"{title}.md")
        filepath = Path("docs") / filename

        if not filepath.exists():
            # 尝试匹配
            candidates = list(Path("docs").glob(f"*{title}*.md"))
            if candidates:
                filepath = candidates[0]
            else:
                print(f"  ❌ {title}: 找不到文档文件")
                continue

        print(f"\n🔄 重试: {title} ({filepath.name})...")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 重新提取（保留 raw_doc）
            fresh_info = proc.extract_class_info(content, filepath.name)

            # 增强
            enhanced = proc.enhance_with_deepseek(fresh_info)

            # 更新 processed_data 中的条目
            for i, entry in enumerate(processed_data):
                if entry["title"] == title:
                    processed_data[i]["enhancement"] = enhanced.get("enhancement", entry["enhancement"])
                    processed_data[i]["method_enhancements"] = enhanced.get("method_enhancements", entry["method_enhancements"])
                    success += 1
                    print(f"  ✅ {title}: 增强成功")
                    break
        except Exception as e:
            print(f"  ❌ {title}: {e}")

    # 保存更新后的数据
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 已保存更新到 {processed_path}")

    # 重新生成 RAG
    rag_data = []
    for api in processed_data:
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
                "enhancement": method_enhancement,
                "class_enhancement": class_enhancement,
            })

    rag_path = Path("processed_docs/rag_knowledge_base.json")
    with open(rag_path, "w", encoding="utf-8") as f:
        json.dump(rag_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已更新 RAG 知识库到 {rag_path}")

    print(f"\n📊 结果: {success}/{len(failed)} 重试成功")


if __name__ == "__main__":
    from loguru import logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="<level>{level: <8}</level> | {message}",
        level="INFO",
    )
    main()
