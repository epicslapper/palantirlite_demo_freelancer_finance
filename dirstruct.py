import os

PROJECT_ROOT = "."
OUTPUT_FILE = "dir_structure.txt"
IGNORE_DIRS = {".venv", "__pycache__", ".git"}

MAX_DEPTH = 2  # only 2 levels deep

lines = []
lines.append("PROJECT DIRECTORY STRUCTURE (max 2 levels, filtered):\n")

for root, dirs, files in os.walk(PROJECT_ROOT):
    depth = root.count(os.sep) - PROJECT_ROOT.count(os.sep)
    if depth > MAX_DEPTH:
        continue

    # filter out ignored directories
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

    indent = "    " * depth
    lines.append(f"{indent}{os.path.basename(root)}/")
    for f in files:
        lines.append(f"{indent}    {f}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Directory structure saved to: {OUTPUT_FILE}")
