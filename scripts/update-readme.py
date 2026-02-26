#!/usr/bin/env python3
"""Auto-update README project tables based on repo topics.

Repos are categorized by topics:
  - "shipped"        → 🚀 Shipped
  - "in-development" → 🔧 In Development
  - "idea"           → 💡 Ideas & Concepts

Repos without these topics or with topic "skip-readme" are excluded.
"""

import json
import os
import re
import subprocess
import sys

OWNER = "gandli"
CATEGORIES = {
    "shipped": [],
    "in-development": [],
    "idea": [],
}


def search_repos_by_topic(topic):
    """Use GitHub search API to find repos with a specific topic."""
    result = subprocess.run(
        ["gh", "api", f"search/repositories?q=user:{OWNER}+topic:{topic}+fork:false&per_page=100",
         "--jq", ".items[] | {name, description, html_url, topics}"],
        capture_output=True, text=True
    )
    repos = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line:
            try:
                r = json.loads(line)
                if r["name"] != OWNER and "skip-readme" not in (r.get("topics") or []):
                    repos.append(r)
            except json.JSONDecodeError:
                pass
    return repos


def build_table(entries, start_num=1):
    if not entries:
        return "| # | Project | Description |\n|---|---------|-------------|\n| - | *Nothing yet* | — |\n"

    lines = ["| # | Project | Description |", "|---|---------|-------------|"]
    for i, e in enumerate(entries, start=start_num):
        desc = e.get("description") or e["name"]
        lines.append(f'| {i} | [{e["name"]}]({e["html_url"]}) | {desc} |')
    return "\n".join(lines) + "\n"


def update_readme(shipped, in_dev, ideas):
    with open("README.md", "r") as f:
        content = f.read()

    def replace_section(content, header, table):
        pattern = rf"(### {re.escape(header)}\n\n)\|.*?(?=\n###|\n---|\Z)"
        return re.sub(pattern, rf"\1{table}", content, flags=re.DOTALL)

    num = 1
    shipped_table = build_table(shipped, num)
    num += max(len(shipped), 0)
    in_dev_table = build_table(in_dev, num)
    num += max(len(in_dev), 0)
    ideas_table = build_table(ideas, num)

    content = replace_section(content, "🚀 Shipped", shipped_table)
    content = replace_section(content, "🔧 In Development", in_dev_table)
    content = replace_section(content, "💡 Ideas & Concepts", ideas_table)

    total = len(shipped) + len(in_dev) + len(ideas)
    content = re.sub(r'\d+ ideas, one commit at a time', f'{total} ideas, one commit at a time', content)
    content = re.sub(r'Ideas-\d+-blue', f'Ideas-{total}-blue', content)

    with open("README.md", "w") as f:
        f.write(content)

    return total


def main():
    shipped = sorted(search_repos_by_topic("shipped"), key=lambda x: x["name"].lower())
    in_dev = sorted(search_repos_by_topic("in-development"), key=lambda x: x["name"].lower())
    ideas = sorted(search_repos_by_topic("idea"), key=lambda x: x["name"].lower())

    print(f"📦 Found: {len(shipped)} shipped, {len(in_dev)} in-dev, {len(ideas)} ideas")

    total = update_readme(shipped, in_dev, ideas)
    print(f"✅ README updated with {total} projects")


if __name__ == "__main__":
    main()
