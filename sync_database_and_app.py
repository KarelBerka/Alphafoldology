import json
import shutil
import re

# 1. Copy tools_data_updated.json to tools_data.json
shutil.copyfile("tools_data_updated.json", "tools_data.json")

with open("tools_data.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print(f"Synced tools_data.json from tools_data_updated.json! Total tools: {len(d['tools'])}")

# 2. Update index.js cache version from v=27 to v=28 (or increment)
with open("index.js", "r", encoding="utf-8") as f:
    content = f.read()

content_new = re.sub(r"tools_data\.json\?v=\d+", "tools_data.json?v=28", content)

with open("index.js", "w", encoding="utf-8") as f:
    f.write(content_new)

print("Updated index.js fetch version to tools_data.json?v=28")
