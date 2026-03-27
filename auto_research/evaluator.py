#!/usr/bin/env python3
"""
Objective Measurement Tool (Eval) for Auto-Research Loop
Evaluates the quality of a SKILL.md against a set of binary criteria.
Outputs a strictly formatted JSON result that the AI Manager can parse.

Fixes applied:
  - CRLF/LF agnostic regex matching (Windows compat)
  - Proper invert logic for no_ai_fluff
  - Per-criterion flag support (MULTILINE, DOTALL)
  - Colored terminal output for quick visual scan
"""
import json
import re
import sys
from pathlib import Path

# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

FLAG_MAP = {
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
    "IGNORECASE": re.IGNORECASE,
}


def load_criteria(evals_path: Path) -> list:
    if not evals_path.exists():
        print(f"{RED}Error: Criteria file not found at {evals_path}{RESET}")
        sys.exit(1)
    with open(evals_path, "r", encoding="utf-8") as f:
        return json.load(f).get("criteria", [])


def evaluate_skill(skill_path: Path, criteria: list) -> dict:
    content = skill_path.read_text(encoding="utf-8")

    results = {}
    passed = 0

    for criterion in criteria:
        criterion_id = criterion["id"]
        regex_pattern = criterion["regex"]
        invert = criterion.get("invert", False)

        # Build flags: default IGNORECASE | MULTILINE | DOTALL
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
        if "flags" in criterion:
            # If explicit flags provided, use only those + IGNORECASE
            flag_str = criterion["flags"]
            flags = re.IGNORECASE
            for flag_name in flag_str.split("|"):
                flag_name = flag_name.strip()
                if flag_name in FLAG_MAP:
                    flags |= FLAG_MAP[flag_name]

        try:
            matched = bool(re.search(regex_pattern, content, flags))
            success = (not matched) if invert else matched

            results[criterion_id] = {
                "question": criterion["question"],
                "success": success,
            }
            if success:
                passed += 1
        except re.error as regex_err:
            results[criterion_id] = {
                "question": criterion["question"],
                "success": False,
                "error": f"Invalid regex: {regex_err}",
            }
        except Exception as exc:
            results[criterion_id] = {
                "question": criterion["question"],
                "success": False,
                "error": str(exc),
            }

    total = len(criteria)
    score = f"{passed}/{total}"

    return {
        "target": str(skill_path),
        "score": score,
        "is_perfect": passed == total,
        "details": results,
    }


def print_report(result: dict) -> None:
    """Pretty-print evaluation results to terminal."""
    target = result["target"]
    score = result["score"]
    is_perfect = result["is_perfect"]

    status_icon = f"{GREEN}✅ PERFECT{RESET}" if is_perfect else f"{RED}❌ FAILING{RESET}"
    print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}Target:{RESET} {target}")
    print(f"{BOLD}Score:{RESET}  {score}  {status_icon}")
    print(f"{CYAN}{'-' * 60}{RESET}")

    for criterion_id, detail in result["details"].items():
        icon = f"{GREEN}✓{RESET}" if detail["success"] else f"{RED}✗{RESET}"
        print(f"  {icon} {criterion_id:<30} {detail['question'][:60]}")
        if "error" in detail:
            print(f"    {YELLOW}⚠ {detail['error']}{RESET}")

    print(f"{CYAN}{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python evaluator.py <path/to/SKILL.md> [--json]")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    json_only = "--json" in sys.argv

    if not skill_path.exists():
        print(f"{RED}Error: Target file not found at {skill_path}{RESET}")
        sys.exit(1)

    eval_file = Path(__file__).parent / "evals.json"
    criteria = load_criteria(eval_file)

    result = evaluate_skill(skill_path, criteria)

    if json_only:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
        # Also output JSON for programmatic consumption
        print(json.dumps(result, indent=2))
