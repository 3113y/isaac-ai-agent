"""
Parse The Binding of Isaac: Repentance log.txt for Lua errors.

Extracts error messages matching:
- "Lua Debug: Error..." or "[Lua] Error..." patterns
- "Stack Traceback" blocks

If the error is simple (syntax, missing end, etc.), attempts auto-fix.
If complex, generates Isaac.DebugString() instrumentation code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Error patterns to match
# ---------------------------------------------------------------------------

_LUA_ERROR_PATTERNS = [
    # Lua Debug: Error in main.lua line 42: ...
    re.compile(
        r"(?:Lua\s*Debug|\[Lua\])\s*:\s*Error[:\s]+"
        r"(?:in\s+(?P<file>[\w./\\]+))?\s*"
        r"(?:line\s+(?P<line>\d+))?[:\s]*"
        r"(?P<message>.+)",
        re.IGNORECASE,
    ),
    # Generic "[ERROR]" log lines
    re.compile(
        r"\[ERROR\]\s*.*?(?:lua|mod)[:\s]*(?P<message>.+)",
        re.IGNORECASE,
    ),
    # "attempt to call" / "attempt to index" runtime errors
    re.compile(
        r"(?:.*:\d+:\s*)?attempt\s+to\s+(?P<message>call\s+(?:a\s+)?\w+\s+.*)",
        re.IGNORECASE,
    ),
    # mod <name> encountered an error
    re.compile(
        r"mod\s+[\"']?(?P<mod_name>\w+)[\"']?\s+encountered\s+(?:an\s+)?error[:\s]*(?P<message>.*)",
        re.IGNORECASE,
    ),
]

_STACK_TRACEBACK_START = re.compile(
    r"Stack\s*Traceback[:\s]*", re.IGNORECASE
)
_STACK_FRAME = re.compile(
    r"^\s*(?P<file>[^:]+):(?P<line>\d+):\s*in\s+(?:function\s+)?[`']?(?P<function>[^'`]+)",
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class LuaError:
    """A parsed Lua error from the log file."""
    raw_line: str
    message: str = ""
    file: Optional[str] = None
    line_number: Optional[int] = None
    stack_trace: List[str] = field(default_factory=list)

    @property
    def is_syntax_error(self) -> bool:
        msg = self.message.lower()
        syntax_keywords = [
            "expected", "unexpected", "missing", "syntax error",
            "malformed", "unclosed", "'end'", "then", "near",
        ]
        return any(kw in msg for kw in syntax_keywords)

    @property
    def is_runtime_error(self) -> bool:
        msg = self.message.lower()
        runtime_keywords = [
            "attempt to call", "attempt to index", "nil value",
            "bad argument", "stack overflow", "cannot",
        ]
        return any(kw in msg for kw in runtime_keywords)

    @property
    def fixable(self) -> bool:
        """Simple errors that can be auto-fixed."""
        return self.is_syntax_error and self.line_number is not None


@dataclass
class LogAnalysisResult:
    """Result of analyzing the Isaac log file."""
    log_path: Optional[str] = None
    errors: List[LuaError] = field(default_factory=list)
    raw_log_tail: str = ""
    fixable_count: int = 0
    total_errors: int = 0


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _extract_stack_trace(lines: list[str], start_idx: int) -> list[str]:
    """Extract stack trace lines starting from a given index."""
    frames = []
    for i in range(start_idx + 1, min(start_idx + 50, len(lines))):
        line = lines[i].strip()
        if not line:
            break
        match = _STACK_FRAME.match(line)
        if match:
            frames.append(
                f"{match.group('file')}:{match.group('line')} "
                f"in {match.group('function')}"
            )
        elif _LUA_ERROR_PATTERNS[0].search(line):
            break  # next error starts
        elif _STACK_TRACEBACK_START.search(line):
            break
        else:
            # Unmatched stack line — might be a continuation
            if frames:
                break  # stop if we already had frames
    return frames


def parse_log_errors(log_path: Optional[str | Path]) -> LogAnalysisResult:
    """Parse the Isaac log file and extract all Lua errors.

    Args:
        log_path: Path to log.txt, or None.

    Returns:
        LogAnalysisResult with extracted errors.
    """
    result = LogAnalysisResult(log_path=str(log_path) if log_path else None)

    if log_path is None:
        return result

    path = Path(log_path)
    if not path.exists():
        logger.warning(f"Log file not found: {log_path}")
        return result

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except (PermissionError, OSError) as e:
        logger.error(f"Cannot read log file: {e}")
        return result

    # Keep the tail of the log for context
    lines = content.splitlines()
    result.raw_log_tail = "\n".join(lines[-200:])  # last 200 lines

    # Scan for error patterns
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        matched = False
        for pattern in _LUA_ERROR_PATTERNS:
            m = pattern.search(line)
            if m:
                error = LuaError(
                    raw_line=line,
                    message=m.groupdict().get("message", line),
                    file=m.groupdict().get("file"),
                    line_number=(
                        int(ln) if (ln := m.groupdict().get("line")) else None
                    ),
                )
                # Check if the next lines are a stack trace
                if i + 1 < len(lines) and _STACK_TRACEBACK_START.search(lines[i + 1]):
                    error.stack_trace = _extract_stack_trace(lines, i + 1)
                result.errors.append(error)
                matched = True
                break

        if not matched and _STACK_TRACEBACK_START.search(line):
            # Standalone stack trace (from a crash dump)
            frames = _extract_stack_trace(lines, i)
            if frames:
                result.errors.append(LuaError(
                    raw_line=line,
                    message="Stack traceback (crash dump)",
                    stack_trace=frames,
                ))

        i += 1

    result.total_errors = len(result.errors)
    result.fixable_count = sum(1 for e in result.errors if e.fixable)

    logger.info(
        f"Log analysis: {result.total_errors} errors, "
        f"{result.fixable_count} potentially fixable"
    )
    return result


# ---------------------------------------------------------------------------
# Auto-fix heuristics
# ---------------------------------------------------------------------------

_SYNTAX_FIX_PATTERNS = [
    # Missing 'end' / 'until' / closing bracket
    (
        re.compile(
            r"expected\s+(?:near\s+)?(?:<eof>|end of file).*?missing\s+(\w+)",
            re.IGNORECASE,
        ),
        lambda m, code: code.rstrip() + f"\n{m.group(1)}\n",
    ),
    # "unexpected symbol near 'x'" — often a missing separator or keyword
    (
        re.compile(
            r"unexpected\s+symbol\s+near\s+['\"](.+?)['\"]",
            re.IGNORECASE,
        ),
        lambda m, code: _fix_unexpected_symbol(m.group(1), code),
    ),
]


def _fix_unexpected_symbol(symbol: str, code: str) -> str:
    """Heuristic fix for 'unexpected symbol near X' errors."""
    if symbol in ("end", "until", "else", "elseif"):
        # Likely a missing block closer before this keyword
        return code
    if symbol in ("then", "do"):
        # If 'then' is unexpected, an 'if' might be malformed
        return code
    return code


def attempt_auto_fix(error: LuaError, lua_code: str) -> Optional[str]:
    """Attempt to auto-fix a Lua error given the existing code.

    Args:
        error: The parsed LuaError.
        lua_code: The full Lua source code.

    Returns:
        Fixed code string if fixable, None otherwise.
    """
    if not error.fixable:
        return None

    # Missing 'end' — count and balance
    if "missing" in error.message.lower() or "unclosed" in error.message.lower():
        fixed = _balance_end_statements(lua_code)
        if fixed != lua_code:
            logger.info("Auto-fix: balanced end statements")
            return fixed

    # "expected near" — try to insert missing syntax
    for pattern, fix_fn in _SYNTAX_FIX_PATTERNS:
        m = pattern.search(error.message)
        if m:
            try:
                fixed = fix_fn(m, lua_code)
                if fixed != lua_code:
                    logger.info(f"Auto-fix: applied syntax fix for '{error.message[:60]}'")
                    return fixed
            except Exception:
                pass

    logger.info(f"Error not auto-fixable: {error.message[:80]}")
    return None


def _balance_end_statements(code: str) -> str:
    """Add missing 'end' statements by counting block openers."""
    import re as _re
    openers = _re.findall(
        r'\b(function|if|for|while|do|repeat)\b',
        code,
    )
    closers = _re.findall(r'\b(end|until)\b', code)

    # repeat...until is a special pair
    repeat_count = sum(1 for o in openers if o == "repeat")
    until_count = sum(1 for c in closers if c == "until")

    # Normal openers require 'end'
    open_count = len(openers) - repeat_count
    close_count = len(closers) - until_count

    end_count = sum(1 for c in closers if c == "end")

    missing_ends = open_count - end_count
    if missing_ends > 0 and missing_ends <= 20:
        return code.rstrip() + "\n" + "end\n" * missing_ends

    return code


# ---------------------------------------------------------------------------
# Debug instrumentation
# ---------------------------------------------------------------------------

def generate_debug_code(
    error: LuaError,
    source_code: str,
    mod_name: str = "isaac_mod",
) -> str:
    """Generate instrumented code with Isaac.DebugString() calls.

    When an error can't be auto-fixed, inject debug output statements
    around the suspected area so the user can see what's happening.

    Args:
        error: The LuaError to instrument around.
        source_code: The original Lua source code.
        mod_name: Name of the mod for context.

    Returns:
        Instrumented Lua code with DebugString calls.
    """
    lines = source_code.split("\n")

    if error.line_number and 1 <= error.line_number <= len(lines):
        target = error.line_number
    else:
        target = len(lines) // 2  # Default to middle of file

    # Inject debug print before and after the suspect area
    debug_before = f'Isaac.DebugString("[DEBUG {mod_name}] Entering suspect area (line {target})")'
    debug_after = f'Isaac.DebugString("[DEBUG {mod_name}] Exited suspect area (line {target})")'

    # Also add variable dump if it's a "nil value" error
    extra_debug = []
    if "nil value" in error.message.lower() or "attempt to index" in error.message.lower():
        # Extract the variable name being indexed
        nil_match = re.search(
            r"attempt\s+to\s+(?:call|index)\s+(?:a\s+)?(\w+)\s+",
            error.message,
            re.IGNORECASE,
        )
        if nil_match:
            var_name = nil_match.group(1)
            extra_debug.append(
                f'Isaac.DebugString("[DEBUG {mod_name}] {var_name} = " .. tostring({var_name}))'
            )

    # Insert debug lines around the target area
    start = max(0, target - 2)
    instrumented = (
        lines[:start]
        + [debug_before]
        + extra_debug
        + lines[start:target]
        + [debug_after]
        + lines[target:]
    )

    return "\n".join(instrumented)


def analyze_and_suggest(
    log_path: Optional[str | Path],
    source_code: str,
    mod_name: str = "isaac_mod",
) -> dict:
    """Full analysis pipeline: parse log, try fixes, generate debug code.

    Returns a dict with:
        - errors: list of parsed error dicts
        - fixable: bool
        - fixed_code: fixed Lua if fixable, else None
        - debug_code: instrumented Lua if not fixable, else None
        - summary: human-readable summary
    """
    result = parse_log_errors(log_path)

    if not result.errors:
        return {
            "errors": [],
            "fixable": False,
            "fixed_code": None,
            "debug_code": None,
            "summary": "No Lua errors found in log file.",
        }

    # Try to fix the first fixable error
    for error in result.errors:
        if error.fixable:
            fixed = attempt_auto_fix(error, source_code)
            if fixed:
                return {
                    "errors": [
                        {
                            "message": e.message,
                            "line": e.line_number,
                            "file": e.file,
                            "fixable": e.fixable,
                            "stack_trace": e.stack_trace,
                        }
                        for e in result.errors
                    ],
                    "fixable": True,
                    "fixed_code": fixed,
                    "debug_code": None,
                    "summary": f"Auto-fixed error: {error.message[:100]}",
                }

    # Not auto-fixable — generate debug instrumentation
    primary_error = result.errors[0]
    debug_code = generate_debug_code(primary_error, source_code, mod_name)

    return {
        "errors": [
            {
                "message": e.message,
                "line": e.line_number,
                "file": e.file,
                "fixable": e.fixable,
                "stack_trace": e.stack_trace,
            }
            for e in result.errors
        ],
        "fixable": False,
        "fixed_code": None,
        "debug_code": debug_code,
        "summary": (
            f"Cannot auto-fix. Injected Isaac.DebugString() calls "
            f"around line {primary_error.line_number or '?'}. "
            f"Check log.txt for debug output."
        ),
    }
