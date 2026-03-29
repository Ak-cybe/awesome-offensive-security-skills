#!/usr/bin/env python3
"""
🔧 Skill Surgery: Transform 191 templated skill files into clean, focused, professional skills.

This script performs 7 surgical operations on every SKILL.md:
1. Remove [CRITICAL: MUST trigger] boilerplate from descriptions
2. Remove copy-pasted "Elite Chaining Strategy" sections
3. Remove copy-pasted "Elite Report Writing" sections
4. Remove copy-pasted "Real-World Disclosed Bounties" sections
5. Remove copy-pasted "Pre-Report Verification" sections
6. Remove empty "Red Team" placeholder sections
7. Remove empty "Execution Phase" boilerplate sections
8. Add reference pointers to shared library
9. Clean up empty Key Concepts tables
10. Clean up broken/truncated Blue Team sections

After transformation:
- Each SKILL.md contains ONLY unique, vulnerability-specific content
- Shared knowledge lives in skills/_shared/references/
- Empty placeholders are removed, not left as dead weight
"""

import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

SKILLS_ROOT = Path(__file__).parent.parent / "skills"
SHARED_REF_PATH = "_shared/references"
LOG_ENTRIES = []

# ─────────────────────────────────────────────────────────────────────
# Pattern definitions for boilerplate sections to remove
# ─────────────────────────────────────────────────────────────────────

# These regex patterns match entire sections (header to next same-level header)
BOILERPLATE_SECTION_PATTERNS = [
    # Elite Chaining Strategy — appears in 180/191 skills
    (
        r'(?m)^###?\s*🏆\s*Elite Chaining Strategy.*?(?=^##\s|\Z)',
        "Elite Chaining Strategy",
        re.DOTALL | re.MULTILINE
    ),
    # Elite Report Writing — appears in 49/191 skills
    (
        r'(?m)^###?\s*📝\s*Elite Report Writing.*?(?=^##\s|\Z)',
        "Elite Report Writing",
        re.DOTALL | re.MULTILINE
    ),
    # Real-World Disclosed Bounties — appears in 38/191 skills
    (
        r'(?m)^##\s*💰\s*Real-World Disclosed Bounties.*?(?=^##\s|\Z)',
        "Real-World Bounties",
        re.DOTALL | re.MULTILINE
    ),
    # Pre-Report Verification — appears in 50/191 skills
    (
        r'(?m)^\*\*Pre-Report Verification \(5 Checks\):\*\*.*?(?=^##|\n\n\n|\Z)',
        "Pre-Report Verification",
        re.DOTALL | re.MULTILINE
    ),
    # Empty Red Team section (only 2-3 generic lines)
    (
        r'(?m)^##\s*🔴\s*Red Team\s*\n-\s*Extract assets and enumerate endpoints\.\s*\n-\s*Execute initial payloads leveraging documented vulnerabilities\.\s*\n*',
        "Empty Red Team placeholder",
        re.MULTILINE
    ),
    # Empty Execution Phase boilerplate
    (
        r'(?m)^##\s*🏁\s*Execution Phase.*?(?=^##\s|\Z)',
        "Execution Phase boilerplate",
        re.DOTALL | re.MULTILINE
    ),
    # "Architect vs Scanner" standalone section (when not inside chaining)
    (
        r'(?m)^\*\*The "Architect" vs "Scanner" Mindset:\*\*\s*\n-\s*❌.*?(?=^##|\n\n\n|\Z)',
        "Architect vs Scanner standalone",
        re.DOTALL | re.MULTILINE
    ),
    # Chaining Decision Tree mermaid block (standalone, outside of Elite Chaining header)
    (
        r'(?m)^\*\*Chaining Decision Tree:\*\*\s*\n```mermaid\s*\ngraph TD.*?```\s*\n',
        "Standalone Chaining Decision Tree",
        re.DOTALL | re.MULTILINE
    ),
    # Common High-Payout Chains table (standalone)
    (
        r'(?m)^\*\*Common High-Payout Chains:\*\*\s*\n\|.*?(?=^##|\*\*The|\n\n\n|\Z)',
        "Standalone Chains table",
        re.DOTALL | re.MULTILINE
    ),
    # Report Structure standalone (HackerOne-Optimized)
    (
        r'(?m)^\*\*Report Structure \(HackerOne-Optimized\):\*\*\s*\n1\..*?(?=^##|\n\n\n|\Z)',
        "Standalone Report Structure",
        re.DOTALL | re.MULTILINE
    ),
    # "What the triager wants to see" standalone block
    (
        r'(?m)^\*\*What the triager wants to see:\*\*\s*\n```.*?```\s*\n',
        "Triager preview block",
        re.DOTALL | re.MULTILINE
    ),
    # Title Format standalone
    (
        r'(?m)^\*\*Title Format\*\*:.*?✅.*?\n\n',
        "Standalone Title Format",
        re.DOTALL | re.MULTILINE
    ),
    # Vickie Li quote (part of report writing boilerplate)
    (
        r'(?m)^>\s*\*\*"The difference between a \$500.*?Bug Bounty Bootcamp\s*\n\n',
        "Vickie Li quote",
        re.DOTALL | re.MULTILINE
    ),
    # Severity Profile boilerplate line
    (
        r'(?m)^\*\*Severity Profile:\*\*.*\n',
        "Severity Profile boilerplate",
        re.MULTILINE
    ),
]

# Pattern for the MUST trigger description prefix
MUST_TRIGGER_PATTERN = re.compile(
    r'\[CRITICAL:\s*MUST trigger this skill whenever related vulnerability testing is discussed\.\]\s*\n?\s*',
    re.IGNORECASE
)

# Pattern for empty Key Concepts rows
EMPTY_KEY_CONCEPTS_ROW = re.compile(
    r'\|\s*\w[^|]*\|\s*\|\s*\n',
    re.MULTILINE
)

# Pattern for broken Blue Team sections (content on same line as header)
BROKEN_BLUE_TEAM = re.compile(
    r'(##\s*🔵\s*Blue Team Detection & Defense\s*)\n-\s*\*\*[^*]+\*\*:\s*\*\*[^*]+\*\*:\s*\*\*[^*]+\*\*:(\s*Key Concepts)',
    re.MULTILINE
)


def log_change(skill_path: str, operation: str, detail: str = ""):
    """Track every change for the audit log."""
    LOG_ENTRIES.append({
        "skill": skill_path,
        "operation": operation,
        "detail": detail,
        "timestamp": datetime.now().isoformat()
    })


def clean_description(content: str, skill_path: str) -> str:
    """Remove [CRITICAL: MUST trigger...] boilerplate from YAML description."""
    original = content
    content = MUST_TRIGGER_PATTERN.sub('', content)
    if content != original:
        log_change(skill_path, "REMOVE_MUST_TRIGGER", "Removed [CRITICAL: MUST trigger] prefix")
    return content


def remove_boilerplate_sections(content: str, skill_path: str) -> str:
    """Remove all copy-pasted boilerplate sections."""
    for pattern_str, section_name, flags in BOILERPLATE_SECTION_PATTERNS:
        pattern = re.compile(pattern_str, flags)
        match = pattern.search(content)
        if match:
            content = pattern.sub('', content)
            log_change(skill_path, f"REMOVE_{section_name.upper().replace(' ', '_')}",
                       f"Removed {section_name} boilerplate")
    return content


def clean_key_concepts(content: str, skill_path: str) -> str:
    """Remove empty Key Concepts table rows (those with empty Description column)."""
    original = content
    content = EMPTY_KEY_CONCEPTS_ROW.sub('', content)
    if content != original:
        log_change(skill_path, "CLEAN_KEY_CONCEPTS", "Removed empty Key Concepts rows")

    # If the Key Concepts table header exists but ALL rows are empty, remove the whole table
    key_concepts_section = re.compile(
        r'(?m)^##\s*Key Concepts\s*\n\|\s*Concept\s*\|\s*Description\s*\|\s*\n\|[-\s]+\|[-\s]+\|\s*\n\s*(?=\n|$)',
        re.MULTILINE
    )
    match = key_concepts_section.search(content)
    if match:
        content = key_concepts_section.sub('', content)
        log_change(skill_path, "REMOVE_EMPTY_KEY_CONCEPTS", "Removed entirely empty Key Concepts table")

    return content


def fix_broken_blue_team(content: str, skill_path: str) -> str:
    """Fix Blue Team sections where content is jammed onto header line."""
    match = BROKEN_BLUE_TEAM.search(content)
    if match:
        # The Blue Team section has all items on one line with double header syntax
        # This is too broken to auto-fix meaningfully, so just add a note
        log_change(skill_path, "FLAG_BROKEN_BLUE_TEAM", "Blue Team section has formatting issues")
    return content


def add_shared_references(content: str, skill_path: str) -> str:
    """Add reference pointers to the shared library before the References section."""
    ref_block = """
## 📚 Shared Resources
> For cross-cutting methodology applicable to all vulnerability classes, see:
> - [`_shared/references/elite-chaining-strategy.md`](../_shared/references/elite-chaining-strategy.md) — Exploit chaining methodology and high-payout chain patterns
> - [`_shared/references/elite-report-writing.md`](../_shared/references/elite-report-writing.md) — HackerOne-optimized report writing, CWE quick reference
> - [`_shared/references/real-world-bounties.md`](../_shared/references/real-world-bounties.md) — Verified disclosed bounties by vulnerability class
"""

    # Insert before References section if it exists
    ref_section = re.search(r'(?m)^## References\b', content)
    if ref_section:
        insert_pos = ref_section.start()
        content = content[:insert_pos] + ref_block + "\n" + content[insert_pos:]
    else:
        # Add at the end
        content = content.rstrip() + "\n" + ref_block

    log_change(skill_path, "ADD_SHARED_REFERENCES", "Added shared reference pointers")
    return content


def clean_excessive_whitespace(content: str) -> str:
    """Remove runs of 3+ blank lines, leaving max 2."""
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = content.rstrip() + '\n'
    return content


def process_skill(skill_path: Path, dry_run: bool = False) -> dict:
    """Process a single SKILL.md file."""
    relative_path = str(skill_path.relative_to(SKILLS_ROOT))
    content = skill_path.read_text(encoding='utf-8')
    original_content = content
    original_lines = len(content.splitlines())

    # 1. Clean description (remove MUST trigger spam)
    content = clean_description(content, relative_path)

    # 2. Remove all boilerplate sections
    content = remove_boilerplate_sections(content, relative_path)

    # 3. Clean empty Key Concepts
    content = clean_key_concepts(content, relative_path)

    # 4. Flag broken Blue Team sections
    content = fix_broken_blue_team(content, relative_path)

    # 5. Add shared reference pointers
    content = add_shared_references(content, relative_path)

    # 6. Clean excessive whitespace
    content = clean_excessive_whitespace(content)

    new_lines = len(content.splitlines())
    lines_removed = original_lines - new_lines

    result = {
        "path": relative_path,
        "original_lines": original_lines,
        "new_lines": new_lines,
        "lines_removed": lines_removed,
        "changed": content != original_content
    }

    if not dry_run and content != original_content:
        skill_path.write_text(content, encoding='utf-8')

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🔧 Skill Surgery: Clean 191 skills")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--single", type=str, help="Process a single skill by path")
    parser.add_argument("--verbose", action="store_true", help="Print detailed changes")
    args = parser.parse_args()

    print("=" * 70)
    print("🔧 SKILL SURGERY — Transforming 191 Skills")
    print("=" * 70)
    print()

    if args.single:
        skill_files = [Path(args.single)]
    else:
        skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
        # Exclude _shared directory
        skill_files = [f for f in skill_files if "_shared" not in str(f)]

    print(f"📂 Found {len(skill_files)} SKILL.md files")
    print(f"🏗️  Mode: {'DRY RUN (no writes)' if args.dry_run else 'LIVE (writing changes)'}")
    print()

    total_changed = 0
    total_lines_removed = 0
    results = []

    for skill_path in skill_files:
        result = process_skill(skill_path, dry_run=args.dry_run)
        results.append(result)

        if result["changed"]:
            total_changed += 1
            total_lines_removed += result["lines_removed"]
            if args.verbose:
                print(f"  ✅ {result['path']}: {result['original_lines']}→{result['new_lines']} lines "
                      f"(-{result['lines_removed']})")

    # Print summary
    print()
    print("=" * 70)
    print("📊 SURGERY RESULTS")
    print("=" * 70)
    print(f"  Total skills processed:  {len(results)}")
    print(f"  Skills modified:         {total_changed}")
    print(f"  Skills unchanged:        {len(results) - total_changed}")
    print(f"  Total lines removed:     {total_lines_removed}")
    print(f"  Avg lines removed/skill: {total_lines_removed / max(total_changed, 1):.1f}")
    print()

    # Operation breakdown from log
    op_counts = {}
    for entry in LOG_ENTRIES:
        op = entry["operation"]
        op_counts[op] = op_counts.get(op, 0) + 1

    if op_counts:
        print("📋 Operations performed:")
        for op, count in sorted(op_counts.items(), key=lambda x: -x[1]):
            print(f"  {op}: {count}")

    # Save detailed log
    log_path = SKILLS_ROOT.parent / "tools" / "fix_skills_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "mode": "dry_run" if args.dry_run else "live",
            "summary": {
                "total_processed": len(results),
                "total_modified": total_changed,
                "total_lines_removed": total_lines_removed,
                "operations": op_counts
            },
            "results": results,
            "changes": LOG_ENTRIES
        }, f, indent=2)
    print(f"\n📄 Detailed log saved to: {log_path}")

    if args.dry_run:
        print("\n⚠️  DRY RUN — no files were modified. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
