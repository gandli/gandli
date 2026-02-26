#!/usr/bin/env python3
"""Auto-update README project tables based on repo topics.

Repos are categorized by topics:
  - "shipped"        → 🚀 Shipped
  - "in-development" → 🔧 In Development
  - "idea"           → 💡 Ideas & Concepts
"""

import json
import re
import subprocess
import sys

OWNER = "gandli"


def get_repos():
    """Fetch all non-fork public repos via list endpoint (works with GITHUB_TOKEN)."""
    result = subprocess.run(
        ["gh", "api", "--paginate", f"users/{OWNER}/repos?per_page=100&type=public"],
        capture_output=True, text=True
    )
    try:
        repos = json.loads(result.stdout)
    except json.JSONDecodeError:
        # --paginate may concat multiple JSON arrays, handle that
        text = result.stdout.strip()
        if text.startswith("[") and "][" in text:
            text = text.replace("][", ",")
        repos = json.loads(text)

    out = {"shipped": [], "in-development": [], "idea": []}
    for r in repos:
        if r.get("fork") or r["name"] == OWNER:
            continue
        topics = r.get("topics") or []
        if "skip-readme" in topics:
            continue
        entry = {
            "name": r["name"],
            "description": r.get("description") or r["name"],
            "html_url": r["html_url"],
        }
        for cat in out:
            if cat in topics:
                out[cat].append(entry)
                break

    for cat in out:
        out[cat].sort(key=lambda x: x["name"].lower())
    return out


def build_table(entries, start_num=1):
    if not entries:
        return "| # | Project | Description |\n|---|---------|-------------|\n| - | *Nothing yet* | — |\n"
    lines = ["| # | Project | Description |", "|---|---------|-------------|"]
    for i, e in enumerate(entries, start=start_num):
        lines.append(f'| {i} | [{e["name"]}]({e["html_url"]}) | {e["description"]} |')
    return "\n".join(lines) + "\n"


def update_readme(cats):
    with open("README.md", "r") as f:
        content = f.read()

    def replace_section(content, header, table):
        pattern = rf"(### {re.escape(header)}\n\n)\|.*?(?=\n###|\n---|\Z)"
        return re.sub(pattern, rf"\1{table}", content, flags=re.DOTALL)

    num = 1
    for header, key in [("🚀 Shipped", "shipped"), ("🔧 In Development", "in-development"), ("💡 Ideas & Concepts", "idea")]:
        content = replace_section(content, header, build_table(cats[key], num))
        num += len(cats[key])

    total = sum(len(v) for v in cats.values())
    content = re.sub(r'\d+ ideas, one commit at a time', f'{total} ideas, one commit at a time', content)
    content = re.sub(r'Ideas-\d+-blue', f'Ideas-{total}-blue', content)

    with open("README.md", "w") as f:
        f.write(content)
    return total


def main():
    cats = get_repos()
    print(f"📦 Found: {len(cats['shipped'])} shipped, {len(cats['in-development'])} in-dev, {len(cats['idea'])} ideas")
    total = update_readme(cats)
    print(f"✅ README updated with {total} projects")


if __name__ == "__main__":
    main()
