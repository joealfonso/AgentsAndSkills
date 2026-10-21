#!/usr/bin/env python3
"""Fail if any relative Markdown link in the repo points at a missing file."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
broken = []
for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    for link in re.findall(r"\]\(([^)#\s]+)", md.read_text()):
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        if not (md.parent / link).exists():
            broken.append(f"{md.relative_to(ROOT)} -> {link}")
print("\n".join(broken) or "no broken links")
sys.exit(1 if broken else 0)
