#!/usr/bin/env python3
"""Incrementally append repos missing from the README into the Ideas & Concepts table.

The README's domain sections are hand-curated — this script never touches them.
It only finds repos not yet linked anywhere in README.md and appends them to the
Ideas section, sorted by name. Idempotent: already-listed repos are skipped.

Run in CI with GH_TOKEN set; the workflow handles branch/PR creation (never push main).

# ponytail: appends everything to Ideas regardless of category. Proper domain
# placement needs topic→section mapping — add when the Ideas bucket gets large.
"""

import json
import re
import subprocess
import sys

OWNER = "gandli"
README = "README.md"
IDEAS_HEADER = "### 💡 Ideas & Concepts"
NEXT_SECTION = "### 📦 Package Management Contributions"


def fetch_repos():
    result = subprocess.run(
        ["gh", "api", "--paginate", f"users/{OWNER}/repos?per_page=100&type=public"],
        capture_output=True, text=True, check=True,
    )
    text = result.stdout.strip()
    if text.startswith("[") and "][" in text:  # --paginate may concat arrays
        text = text.replace("][", ",")
    return json.loads(text)


def listed_names(readme):
    return set(re.findall(r"github\.com/gandli/([a-zA-Z0-9_.-]+)", readme))


def missing_entries(repos, listed):
    out = []
    for r in repos:
        name = r["name"]
        if r.get("fork") or name == OWNER or name in listed:
            continue
        if "skip-readme" in (r.get("topics") or []):
            continue
        out.append((name, r.get("description") or name))
    out.sort(key=lambda x: x[0].lower())
    return out


def append_ideas(readme, entries):
    header_pos = readme.index(IDEAS_HEADER)
    next_pos = readme.index(NEXT_SECTION, header_pos)
    rows = "".join(
        f"| [{name}](https://github.com/{OWNER}/{name}) | {desc} |\n"
        for name, desc in entries
    )
    return readme[:next_pos] + rows + "\n" + readme[next_pos:]


def main():
    readme = open(README).read()
    entries = missing_entries(fetch_repos(), listed_names(readme))
    if not entries:
        print("No missing repos — README is up to date")
        return 0
    open(README, "w").write(append_ideas(readme, entries))
    print(f"Appended {len(entries)} repos to Ideas section:")
    for name, _ in entries:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
