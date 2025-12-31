import os

PROJECT_ROOT = "."
OUTPUT_FILE = "project_snapshot.txt"

# Automatically include all .py files + models.yaml
RELEVANT_FILES = []

for root, dirs, files in os.walk(PROJECT_ROOT):
    # skip irrelevant directories
    if any(ignored in root for ignored in [".venv", ".idea", "__pycache__"]):
        continue
    for f in files:
        if f.endswith(".py") or f == "models.yaml":
            RELEVANT_FILES.append(os.path.join(root, f))

lines = ["PROJECT SNAPSHOT (all .py files + models.yaml)\n", "="*80 + "\n"]

for filepath in sorted(RELEVANT_FILES):
    relpath = os.path.relpath(filepath, PROJECT_ROOT)
    lines.append(f"--- FILE: {relpath} ---\n")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines.append(f.read() + "\n")
    except Exception as e:
        lines.append(f"ERROR READING FILE: {e}\n\n")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Project snapshot saved to: {OUTPUT_FILE}")
