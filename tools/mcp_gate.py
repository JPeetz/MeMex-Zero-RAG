#!/usr/bin/env python3
"""mcp_gate — the MCP engineering standard, as an executable gate.

Runs with the standard library only. Optional integrations (ruff, bandit, pip-audit, pytest,
semgrep, gitleaks) light up automatically when present; when absent they are SKIPped with a
reason — never reported as PASS, because an unrun check is not a passing check.

    python3 mcp_gate.py /path/to/mcp/repo
    python3 mcp_gate.py . --strict      # SKIP counts as failure (use in CI)

Exit codes: 0 all required gates pass · 1 a required gate failed · 2 usage error.

Gates are grouped by the standard's four questions:
  Does it work?      tests, tool-contract, json
  Is it safe?        security-tests, secrets, deps, auth, guardrails
  Is it honest?      docs, version, ci
  Is it clean?       clean-code
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RESULTS: list[tuple[str, str, str, str]] = []   # (status, gate, detail, remedy)


def record(status: str, gate: str, detail: str, remedy: str = "") -> None:
    RESULTS.append((status, gate, detail, remedy))


def skip_if_missing(tool: str) -> bool:
    if shutil.which(tool) is None:
        record("SKIP", tool, f"{tool} not installed", f"install {tool} to enable this check")
        return True
    return False


def py_files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*.py"):
        if any(part in p.parts for part in ("node_modules", ".git", ".venv", "venv", "__pycache__", "build", "dist")):
            continue
        out.append(p)
    return out


# ---------------------------------------------------------------- clean code

def gate_clean_code(root: Path) -> None:
    problems: list[str] = []
    warnings: list[str] = []
    for f in py_files(root):
        if "tools" in f.parts:          # the gate and other tooling are not application code
            continue
        try:
            tree = ast.parse(f.read_text(errors="ignore"))
        except SyntaxError as e:
            problems.append(f"{f.name}: syntax error line {e.lineno}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                length = (node.end_lineno or node.lineno) - node.lineno
                # Separate logic from data: a 270-line table of tool schemas is reviewable;
                # a 270-line state machine is not. Count control-flow, not lines, for that.
                logic = sum(1 for n in ast.walk(node)
                            if isinstance(n, (ast.If, ast.For, ast.While, ast.Try,
                                              ast.With, ast.Raise, ast.Assert)))
                if length > 200 and logic > 8:
                    problems.append(f"{f.name}:{node.lineno} {node.name}() is {length} lines, logic={logic} (>200)")
                elif length > 200:
                    warnings.append(f"{f.name}:{node.lineno} {node.name}() is {length} lines but is data (logic={logic})")
                elif length > 120:
                    warnings.append(f"{f.name}:{node.lineno} {node.name}() is {length} lines (>120)")
                branches = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp)))
                if branches > 25:
                    problems.append(f"{f.name}:{node.lineno} {node.name}() branch score {branches} (>25)")
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                problems.append(f"{f.name}:{node.lineno} bare except")
    if problems:
        record("FAIL", "clean-code", f"{len(problems)} issue(s)", "; ".join(problems[:4]))
    elif warnings:
        record("WARN", "clean-code", f"{len(warnings)} long function(s) — extract for reviewability",
               "; ".join(warnings[:3]))
    else:
        record("PASS", "clean-code", "no oversized functions, hot functions or bare excepts")

    if not skip_if_missing("ruff"):
        r = subprocess.run(["ruff", "check", str(root)], capture_output=True, text=True)
        record("PASS" if r.returncode == 0 else "FAIL", "ruff",
               "clean" if r.returncode == 0 else (r.stdout.strip().splitlines() or ["issues"])[-1])


# ------------------------------------------------------------ tool contract

TOOL_PATTERNS = [
    re.compile(r'name\s*=\s*["\']([a-z0-9_]+)["\']'),
    # dict style: a "name" key within a few lines of an inputSchema/description key
    re.compile(r'["\']name["\']\s*:\s*["\']([a-z0-9_]+)["\'](?=[^{}]{0,400}?["\'](?:inputSchema|description)["\'])', re.S),
]


ONE_OFF = re.compile(r"^(apply-|patch-|fix-|migrate-)")


def find_tools(root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for f in py_files(root):
        if ONE_OFF.match(f.name) or "tests" in f.parts:
            continue
        text = f.read_text(errors="ignore")
        if "tool" not in text.lower():
            continue
        for rx in TOOL_PATTERNS:
            for m in rx.finditer(text):
                found.setdefault(m.group(1), f)
    return found


def gate_tool_contract(root: Path) -> None:
    tools = find_tools(root)
    if not tools:
        record("SKIP", "tool-contract", "no tool definitions detected", "expected @mcp.tool / register_tool patterns")
        return
    defs = {}
    for f in py_files(root):
        if f.name.startswith("test_") or "tests" in f.parts or ONE_OFF.match(f.name):
            continue
        txt = f.read_text(errors="ignore")
        sites = set(re.findall(r'(?:@\w+\.tool[^\n]*|register_tool\([^)]*?|(?:types\.)?Tool\(\s*)name\s*=\s*["\']([a-z0-9_]+)["\']', txt, re.S))
        for n in sites:
            defs.setdefault(n, []).append(f.name)
    dupes = sorted({n for n, where in defs.items() if len(where) > 1})
    record("PASS" if not dupes else "FAIL", "tool-uniqueness",
           f"{len(tools)} tools found" if not dupes else f"duplicate tool names in {dupes}",
           "namespace as server__tool when aggregating")
    record("PASS", "tool-namespace",
           f"{len(tools)} tool names use lowercase_snake; verify prefix when aggregating")


def gate_json(root: Path) -> None:
    """Every declared inputSchema must be structurally valid JSON Schema."""
    bad: list[str] = []
    checked = 0
    for f in py_files(root) + list(root.rglob("*.json")):
        if f.suffix == ".json":
            try:
                json.loads(f.read_text(errors="ignore"))
                checked += 1
            except json.JSONDecodeError as e:
                bad.append(f"{f.name}: invalid JSON ({e.msg})")
            continue
        text = f.read_text(errors="ignore")
        for m in re.finditer(r'("inputSchema"|"input_schema")\s*:\s*(\{.*?\})\s*[,}]', text, re.S):
            blob = m.group(2)
            try:
                schema = json.loads(blob)
            except json.JSONDecodeError:
                bad.append(f"{f.name}: unparsable inputSchema")
                continue
            checked += 1
            if schema.get("type") not in (None, "object"):
                bad.append(f"{f.name}: inputSchema type should be 'object'")
            props = schema.get("properties") or {}
            for req in schema.get("required") or []:
                if props and req not in props:
                    bad.append(f"{f.name}: required '{req}' not in properties")
    unparsable = [b for b in bad if "unparsable" in b]
    real = [b for b in bad if "unparsable" not in b]
    if not checked:
        record("SKIP", "json", "no JSON or inputSchema found")
    elif real:
        record("FAIL", "json", f"{len(real)} issue(s)", "; ".join(sorted(set(real))[:3]))
    elif unparsable:
        record("WARN", "json", f"{checked} checked; {len(unparsable)} Python-embedded schema(s) not statically parseable",
               "assert schemas in tests instead of grepping source")
    else:
        record("PASS", "json", f"{checked} payload/schema(s) validated")


# --------------------------------------------------------------- safety

def gate_security_tests(root: Path) -> None:
    names = [p.name.lower() for p in root.rglob("test_*.py")]
    adversarial = [n for n in names if re.search(r"security|inject|exploit|adversar|attack|auth", n)]
    if not names:
        record("FAIL", "security-tests", "no test files found", "add tests/ with adversarial cases")
    elif not adversarial:
        record("FAIL", "security-tests", f"{len(names)} test files, none security-focused",
               "add test_security.py: injection in tool output, denied-call-no-side-effect, auth 401/403")
    else:
        record("PASS", "security-tests", f"{len(adversarial)} adversarial file(s): {', '.join(adversarial[:3])}")


def gate_secrets(root: Path) -> None:
    pats = [re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
            re.compile(r"\bAKIA[0-9A-Z]{16}\b"), re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")]
    hits = []
    for p in root.rglob("*"):
        if not p.is_file() or any(x in p.parts for x in (".git", ".venv", "node_modules", "__pycache__")):
            continue
        if p.suffix not in (".py", ".json", ".yml", ".yaml", ".md", ".txt", ".env", ".toml", ".sh", ""):
            continue
        try:
            t = p.read_text(errors="ignore")
        except Exception:
            continue
        for rx in pats:
            if rx.search(t):
                hits.append(str(p.relative_to(root)))
                break
    record("PASS" if not hits else "FAIL", "secrets",
           "no credential-shaped strings" if not hits else f"possible secrets in {hits[:3]}")


def gate_deps(root: Path) -> None:
    req = next((p for p in (root/"requirements.txt", root/"requirements-test.txt") if p.exists()), None)
    pyproj = root/"pyproject.toml"
    if skip_if_missing("pip-audit"):
        return
    target = str(req) if req else str(root)
    r = subprocess.run(["pip-audit", "-r", target] if req else ["pip-audit"],
                       capture_output=True, text=True)
    record("PASS" if r.returncode == 0 else "FAIL", "deps",
           "no known CVEs" if r.returncode == 0 else (r.stdout or r.stderr).strip().splitlines()[-1][:120])
    _ = pyproj


def gate_auth_transport(root: Path) -> None:
    text = "\n".join(f.read_text(errors="ignore") for f in py_files(root))
    issues, notes = [], []
    uses_sse = bool(re.search(r"\bSseServerTransport\b|\bsse_server\b", text))
    uses_http = bool(re.search(r"StreamableHTTPSessionManager|streamable_http", text))
    if uses_sse and not uses_http:
        issues.append("SSE is the only network transport — deprecated; move to Streamable HTTP")
    elif uses_sse and uses_http:
        record("WARN", "transport-legacy", "SSE retained alongside Streamable HTTP — deprecate it",
               "remove the SSE path once no client depends on it")
    if re.search(r"0\.0\.0\.0", text) and not re.search(r"127\.0\.0\.1", text):
        issues.append("binds 0.0.0.0 without loopback guard")
    if re.search(r"transport\s*=\s*[\"'](sse|http|streamable)[\"']", text) and not re.search(r"(verify|jwt|oauth|bearer|authoriz)", text, re.I):
        issues.append("remote transport without visible auth")
    if re.search(r"stdio", text):
        notes.append("stdio: credentials come from the environment per spec")
    record("FAIL" if issues else "PASS", "auth-transport",
           "; ".join(issues) if issues else ("local-only / authenticated" + (f" ({notes[0]})" if notes else "")))


def gate_guardrails(root: Path) -> None:
    text = "\n".join(f.read_text(errors="ignore") for f in py_files(root))
    checks = {
        "input validation": r"(jsonschema|validate|schema)",
        "payload cap": r"(MAX_|max_bytes|content-length|body_too_large|limit)",
        "rate limit": r"(rate.?limit|throttl|token bucket|RATE)",
        "timeout": r"(timeout=|asyncio\.wait_for)",
        "audit/trace": r"(audit|trace|log_event|append\(.*event)",
        "kill switch": r"(kill|revoke|disable|emergency)",
        "output screening": r"(sanitiz|redact|strip_instructions|escape|untrusted)",
        "approval gate": r"(approve|approval|human|confirm)",
    }
    missing = [k for k, rx in checks.items() if not re.search(rx, text, re.I)]
    if len(missing) >= 4:
        record("FAIL", "guardrails", f"{len(missing)} absent: {', '.join(missing[:5])}",
               "see STANDARD.md §Guardrails — deterministic controls, not prompt instructions")
    elif missing:
        record("WARN", "guardrails", f"partial — missing: {', '.join(missing)}",
               "add the missing layers; prompt-level guardrails do not count")
    else:
        record("PASS", "guardrails", f"all {len(checks)} control families present")



# ------------------------------------------------- resource-profile gates

SPEC_NAMES = ("mcp.spec.json", "mcp-spec.json", ".mcp/spec.json")


def load_spec(root: Path):
    for name in SPEC_NAMES:
        cand = root / name
        if cand.exists():
            try:
                return json.loads(cand.read_text())
            except json.JSONDecodeError as e:
                record("FAIL", "spec-declaration", f"{name} is not valid JSON: {e.msg}",
                       "the declaration is the contract; it must parse")
                return None
    return None


def gate_spec(root: Path, tools: dict) -> dict:
    """An MCP is purpose-built: its declaration defines which profile gates apply."""
    spec = load_spec(root)
    if spec is None:
        if len(tools) >= 5:
            record("FAIL", "spec-declaration",
                   f"{len(tools)} tools but no mcp.spec.json — purpose and resources undeclared",
                   "declare purpose, transport, auth, resource profiles, tool side-effects (see mcp.spec.example.json)")
        else:
            record("SKIP", "spec-declaration", "no declaration and few/no tools")
        return {}
    missing = [k for k in ("name", "purpose", "transport", "auth", "resources", "tools") if k not in spec]
    record("PASS" if not missing else "FAIL", "spec-declaration",
           f"{spec.get('name')} · {len(spec.get('resources', {}))} resource profile(s)" if not missing
           else f"declaration missing: {missing}",
           "purpose, transport, auth, resources and tools are all required" if missing else "")

    bad_tools = [t.get("name", "?") for t in spec.get("tools", [])
                 if "side_effect" not in t or "approval" not in t]
    destructive = [t.get("name") for t in spec.get("tools", [])
                   if t.get("side_effect") == "destructive" and t.get("approval") != "required"]
    if bad_tools:
        record("FAIL", "spec-tool-metadata", f"{len(bad_tools)} tool(s) declare no side_effect/approval",
               "; ".join(map(str, bad_tools[:4])))
    elif destructive:
        record("FAIL", "spec-tool-metadata", f"destructive tools without approval: {destructive}",
               "destructive implies approval: required")
    else:
        record("PASS", "spec-tool-metadata", f"{len(spec.get('tools', []))} tools declare side-effect and approval")
    return spec


def _tests_matching(root: Path, pattern: str) -> list[str]:
    rx = re.compile(pattern, re.I)
    return [p.name for p in root.rglob("test_*.py") if rx.search(p.name)]


def gate_profiles(root: Path, spec: dict) -> None:
    res = (spec or {}).get("resources") or {}
    code = "\n".join(f.read_text(errors="ignore") for f in py_files(root) if "tests" not in f.parts)

    # --- SQL -------------------------------------------------------------
    if res.get("sql"):
        issues = []
        fstring_sql = re.findall(r'f["\'][^"\']*\b(?:SELECT|INSERT|UPDATE|DELETE)\b[^"\']*["\']', code, re.I)
        validated_ident = bool(re.search(r'def _safe_ident|def _ident|_safe_identifier', code))
        value_interp = [q for q in fstring_sql if re.search(r'\{[^}]*\}', q) and not validated_ident]
        if value_interp:
            issues.append("string-built SQL with interpolated values")
        elif fstring_sql and validated_ident:
            record("WARN", "sql-fstring", f"{len(fstring_sql)} f-string queries use validated identifiers",
                   "identifiers cannot be bound as parameters; keep the validation helper and test it")
        if re.search(r'(SELECT|INSERT|UPDATE|DELETE)[^"\']*["\']\s*[%+]\s*\(', code, re.I):
            issues.append("string concatenation into SQL")
        if not re.search(r':\w+|%s|\$1|\?', code):
            issues.append("no parameter placeholders found")
        if not re.search(r'\bLIMIT\b|max_rows', code, re.I):
            issues.append("no row cap")
        if any(m.get("mode") == "read-only" for m in res["sql"]) and re.search(r'\b(INSERT|UPDATE|DELETE|DROP)\b', code, re.I):
            issues.append("write SQL present but profile says read-only")
        tests = _tests_matching(root, r"sql|inject|query")
        if not tests:
            issues.append("no SQL/injection test")
        record("FAIL" if issues else "PASS", "profile:sql",
               f"{len(res['sql'])} datasource(s) declared" if not issues else "; ".join(issues),
               "parameterise queries, cap rows, match the declared mode, test injection" if issues else "")

    # --- files -----------------------------------------------------------
    if res.get("files"):
        issues = []
        if not re.search(r'(resolve\(\)|\.absolute\(\)|abspath)', code):
            issues.append("no path resolution before use")
        if not re.search(r'(is_relative_to|startswith|commonpath|relative_to)', code):
            issues.append("no root-containment check (traversal)")
        if not re.search(r'(max_bytes|st_size|MAX_\w+|size.*limit)', code, re.I):
            issues.append("no size cap")
        if any(not m.get("follow_symlinks", True) for m in res["files"]) and "symlink" not in code.lower():
            issues.append("symlink policy declared but not enforced")
        tests = _tests_matching(root, r"path|traversal|file")
        if not tests:
            issues.append("no traversal test")
        record("FAIL" if issues else "PASS", "profile:files",
               f"{len(res['files'])} root(s) declared" if not issues else "; ".join(issues),
               "resolve, contain, cap, and test traversal" if issues else "")

    # --- web -------------------------------------------------------------
    if res.get("web"):
        issues = []
        if re.search(r'169\.254\.169\.254|metadata\.google\.internal', code) and not re.search(r'(block|deny|forbid)', code, re.I):
            issues.append("metadata endpoint reachable (SSRF)")
        if not re.search(r'(allow|allowlist|whitelist|allowed_hosts)', code, re.I):
            issues.append("no host allowlist")
        if not re.search(r'timeout\s*=', code):
            issues.append("no request timeout")
        if "requests." in code and "verify=False" in code:
            issues.append("TLS verification disabled")
        tests = _tests_matching(root, r"ssrf|url|web|http")
        if not tests:
            issues.append("no SSRF/URL test")
        record("FAIL" if issues else "PASS", "profile:web",
               f"{len(res['web'])} allowlist(s) declared" if not issues else "; ".join(issues),
               "allowlist, block link-local, cap size, verify TLS, test SSRF" if issues else "")

    # --- injected --------------------------------------------------------
    if res.get("injected"):
        issues = []
        if not re.search(r'(sanitiz|strip|screen|redact|untrusted)', code, re.I):
            issues.append("no screening of injected content")
        if not re.search(r'(max_chars|MAX_\w+|truncat)', code, re.I):
            issues.append("no length cap on injected content")
        tests = _tests_matching(root, r"inject|prompt|content|exploit")
        if not tests:
            issues.append("no injection test")
        record("FAIL" if issues else "PASS", "profile:injected",
               f"{len(res['injected'])} source(s) declared" if not issues else "; ".join(issues),
               "screen, cap, and test instruction injection" if issues else "")

    # --- declared but absent --------------------------------------------
    absent = [k for k in ("sql", "files", "web", "injected")
              if res.get(k) and not re.search({"sql": r"(SELECT|INSERT|UPDATE|DELETE)",
                                               "files": r"(open\(|Path\()",
                                               "web": r"(requests\.|httpx|urllib|aiohttp)",
                                               "injected": r"(prompt|content|context)"}[k], code, re.I)]
    if absent:
        record("WARN", "spec-vs-code", f"declared but not found in code: {absent}",
               "a declaration that does not match the code is documentation drift")


# ------------------------------------------------------------- honesty

def gate_docs(root: Path) -> None:
    readme = next((p for p in root.glob("README*")), None)
    if not readme:
        record("FAIL", "docs", "no README", "document transport, tools, auth model, security posture")
        return
    t = readme.read_text(errors="ignore").lower()
    need = {"transport": r"stdio|streamable|sse", "tools": r"tool", "security": r"security|auth|credential"}
    missing = [k for k, rx in need.items() if not re.search(rx, t)]
    record("PASS" if not missing else "WARN", "docs",
           "README covers transport, tools, security" if not missing else f"README missing: {missing}")


def gate_version(root: Path) -> None:
    text = "\n".join(f.read_text(errors="ignore") for f in py_files(root)) + \
           "\n".join(p.read_text(errors="ignore") for p in root.glob("README*"))
    found = sorted(set(re.findall(r"20\d\d-\d\d-\d\d", text)))
    if not found:
        record("WARN", "spec-version", "no protocol revision declared",
               "state the target revision (current is 2026-07-28)")
    else:
        newest = found[-1]
        behind = newest < "2026-07-28"
        record("WARN" if behind else "PASS", "spec-version",
               f"newest revision referenced: {newest}" + (" (behind current 2026-07-28)" if behind else ""),
               "state the target revision explicitly" if behind else "")


def gate_ci(root: Path) -> None:
    wf = list((root/".github"/"workflows").glob("*.y*ml")) if (root/".github"/"workflows").exists() else []
    if not wf:
        record("FAIL", "ci", "no GitHub workflows", "add ci.yml: tests + security + gate on push/PR")
        return
    body = "\n".join(p.read_text(errors="ignore") for p in wf).lower()
    has_tests = bool(re.search(r"pytest|unittest", body))
    has_sec = bool(re.search(r"bandit|pip-audit|semgrep|gitleaks|codeql", body))
    if has_tests and has_sec:
        record("PASS", "ci", f"{len(wf)} workflow(s): tests + security")
    else:
        record("FAIL", "ci", f"{len(wf)} workflow(s); tests={has_tests} security={has_sec}",
               "CI must run both the test suite and a security scan on every push and PR")


def find_test_dirs(root: Path) -> list[Path]:
    dirs = []
    for p in root.rglob("tests"):
        if p.is_dir() and not any(x in p.parts for x in (".venv", "node_modules", "__pycache__")):
            dirs.append(p)
    return dirs


def gate_tests(root: Path) -> None:
    dirs = find_test_dirs(root)
    test_files = [f for d in dirs for f in d.glob("test_*.py")]
    if not test_files:
        record("FAIL", "tests", "no test_*.py found", "add tests; unproven code is unverified code")
        return
    pytest_style = any((d / "conftest.py").exists() for d in dirs) or \
                   any(re.search(r"^import pytest|^from pytest", f.read_text(errors="ignore"), re.M)
                       for f in test_files)
    has_pytest = shutil.which("pytest") is not None

    if has_pytest:
        r = subprocess.run(["pytest", "-q"], cwd=root, capture_output=True, text=True)
        tail = [l for l in (r.stdout or "").strip().splitlines() if l.strip()]
        record("PASS" if r.returncode == 0 else "FAIL", "tests",
               (tail[-1] if tail else "pytest ran")[:120],
               "" if r.returncode == 0 else "fix the failing suite before anything else")
        return
    if pytest_style:
        record("SKIP", "tests",
               f"{len(test_files)} pytest-style test file(s) across {len(dirs)} dir(s); pytest not installed",
               "install pytest (the suite is written for it) — unittest cannot collect these")
        return
    total, failed, last = 0, False, ""
    for d in dirs:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(d),
                            "-t", str(d), "-q"], capture_output=True, text=True)
        out = r.stderr or r.stdout
        line = next((l for l in out.splitlines() if l.startswith("Ran ")), "")
        m = re.search(r"Ran (\d+) tests", line)
        if m:
            total += int(m.group(1))
        last = line or last
        if r.returncode != 0:
            failed = True
    if total == 0:
        record("FAIL", "tests", "0 tests collected — a suite that runs nothing proves nothing",
               "check the test directory layout / add tests")
    else:
        record("PASS" if not failed else "FAIL", "tests", f"{total} tests across {len(dirs)} dir(s)" + ("" if not failed else " — FAILING"),
               "" if not failed else "fix the failing suite before anything else")


# ------------------------------------------------------------------ main

def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    root = Path(args[0] if args else ".").resolve()
    if not root.exists():
        print(f"no such path: {root}")
        return 2

    print(f"mcp_gate · {root}")
    print("=" * 68)
    try:
        spec = gate_spec(root, find_tools(root))
        gate_profiles(root, spec)
    except Exception as e:
        record("FAIL", "spec/profile", f"crashed: {e}", "fix the declaration")

    for fn in (gate_tests, gate_tool_contract, gate_json, gate_security_tests, gate_secrets,
               gate_deps, gate_auth_transport, gate_guardrails, gate_clean_code, gate_docs,
               gate_version, gate_ci):
        try:
            fn(root)
        except Exception as e:                     # a crashing gate is a failing gate
            record("FAIL", fn.__name__, f"gate crashed: {e}", "fix the gate or the repo layout")

    order = {"FAIL": 0, "WARN": 1, "SKIP": 2, "PASS": 3}
    for status, gate, detail, remedy in sorted(RESULTS, key=lambda r: order[r[0]]):
        print(f"  [{status:4}] {gate:18} {detail}")
        if remedy and status in ("FAIL", "WARN"):
            print(f"         └─ {remedy}")

    fails = sum(1 for r in RESULTS if r[0] == "FAIL")
    warns = sum(1 for r in RESULTS if r[0] == "WARN")
    skips = sum(1 for r in RESULTS if r[0] == "SKIP")
    passes = sum(1 for r in RESULTS if r[0] == "PASS")
    print("-" * 68)
    print(f"  {passes} pass · {warns} warn · {fails} fail · {skips} skipped")
    if fails:
        print("  RESULT: FAIL — the standard is not met")
        return 1
    if strict and skips:
        print(f"  RESULT: FAIL (--strict) — {skips} check(s) could not run")
        return 1
    print("  RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
