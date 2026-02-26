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


def get_repos():
    """Fetch all non-fork repos for the user."""
    result = subprocess.run(
        ["gh", "api", "users/gandli/repos", "--paginate",
         "--jq", '.[] | select(.fork == false) | {name, description, topics, html_url}'],
        capture_output=True, text=True
    )
    repos = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line:
            try:
                repos.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return repos


def categorize(repos):
    shipped = []
    in_dev = []
    ideas = []

    for r in repos:
        topics = r.get("topics", []) or []
        name = r["name"]
        desc = r.get("description") or name
        url = r["html_url"]

        if "skip-readme" in topics or name == "gandli":
            continue

        entry = {"name": name, "desc": desc, "url": url}

        if "shipped" in topics:
            shipped.append(entry)
        elif "in-development" in topics:
            in_dev.append(entry)
        elif "idea" in topics:
            ideas.append(entry)
        # Repos without category topics are skipped

    # Sort alphabetically within each category
    for lst in (shipped, in_dev, ideas):
        lst.sort(key=lambda x: x["name"].lower())

    return shipped, in_dev, ideas


def build_table(entries, start_num=1):
    if not entries:
        return "| # | Project | Description |\n|---|---------|-------------|\n| - | *Nothing yet* | — |\n"

    lines = ["| # | Project | Description |", "|---|---------|-------------|"]
    for i, e in enumerate(entries, start=start_num):
        lines.append(f'| {i} | [{e["name"]}]({e["url"]}) | {e["desc"]} |')
    return "\n".join(lines) + "\n"


def update_readme(shipped, in_dev, ideas):
    with open("README.md", "r") as f:
        content = f.read()

    def replace_section(content, header, table):
        # Match from header to next ### or --- or end
        pattern = rf"(### {re.escape(header)}\n\n)\|.*?(?=\n###|\n---|\Z)"
        replacement = rf"\1{table}"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        return new_content

    num = 1
    shipped_table = build_table(shipped, num)
    num += len(shipped)
    in_dev_table = build_table(in_dev, num)
    num += len(in_dev)
    ideas_table = build_table(ideas, num)

    content = replace_section(content, "🚀 Shipped", shipped_table)
    content = replace_section(content, "🔧 In Development", in_dev_table)
    content = replace_section(content, "💡 Ideas & Concepts", ideas_table)

    # Update the tagline count
    total = len(shipped) + len(in_dev) + len(ideas)
    content = re.sub(
        r'\d+ ideas, one commit at a time',
        f'{total} ideas, one commit at a time',
        content
    )

    # Update Ideas badge count
    content = re.sub(
        r'Ideas-\d+-blue',
        f'Ideas-{total}-blue',
        content
    )

    with open("README.md", "w") as f:
        f.write(content)

    return total


def main():
    repos = get_repos()
    shipped, in_dev, ideas = categorize(repos)

    print(f"📦 Found: {len(shipped)} shipped, {len(in_dev)} in-dev, {len(ideas)} ideas")

    total = update_readme(shipped, in_dev, ideas)
    print(f"✅ README updated with {total} projects")


if __name__ == "__main__":
    main()
