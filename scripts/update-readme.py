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


def search_repos_by_topic(topic):
    """Use GitHub search API to find repos with a specific topic."""
    result = subprocess.run(
        ["gh", "api", f"search/repositories?q=user:{OWNER}+topic:{topic}+fork:false&per_page=100"],
        capture_output=True, text=True
    )
    repos = []
    try:
        data = json.loads(result.stdout)
        for r in data.get("items", []):
            name = r.get("name", "")
            if name == OWNER or "skip-readme" in (r.get("topics") or []):
                continue
            repos.append({
                "name": name,
                "description": r.get("description") or name,
                "html_url": r.get("html_url", f"https://github.com/{OWNER}/{name}"),
            })
    except json.JSONDecodeError as e:
        print(f"⚠️ Failed to parse search results for topic '{topic}': {e}", file=sys.stderr)
    return sorted(repos, key=lambda x: x["name"].lower())


def build_table(entries, start_num=1):
    if not entries:
        return "| # | Project | Description |\n|---|---------|-------------|\n| - | *Nothing yet* | — |\n"

    lines = ["| # | Project | Description |", "|---|---------|-------------|"]
    for i, e in enumerate(entries, start=start_num):
        lines.append(f'| {i} | [{e["name"]}]({e["html_url"]}) | {e["description"]} |')
    return "\n".join(lines) + "\n"


def update_readme(shipped, in_dev, ideas):
    with open("README.md", "r") as f:
        content = f.read()

    def replace_section(content, header, table):
        pattern = rf"(### {re.escape(header)}\n\n)\|.*?(?=\n###|\n---|\Z)"
        return re.sub(pattern, rf"\1{table}", content, flags=re.DOTALL)

    num = 1
    content = replace_section(content, "🚀 Shipped", build_table(shipped, num))
    num += len(shipped)
    content = replace_section(content, "🔧 In Development", build_table(in_dev, num))
    num += len(in_dev)
    content = replace_section(content, "💡 Ideas & Concepts", build_table(ideas, num))

    total = len(shipped) + len(in_dev) + len(ideas)
    content = re.sub(r'\d+ ideas, one commit at a time', f'{total} ideas, one commit at a time', content)
    content = re.sub(r'Ideas-\d+-blue', f'Ideas-{total}-blue', content)

    with open("README.md", "w") as f:
        f.write(content)
    return total


def main():
    shipped = search_repos_by_topic("shipped")
    in_dev = search_repos_by_topic("in-development")
    ideas = search_repos_by_topic("idea")

    print(f"📦 Found: {len(shipped)} shipped, {len(in_dev)} in-dev, {len(ideas)} ideas")
    total = update_readme(shipped, in_dev, ideas)
    print(f"✅ README updated with {total} projects")


if __name__ == "__main__":
    main()
