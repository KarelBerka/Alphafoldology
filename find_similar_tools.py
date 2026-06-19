import json

db_path = "tools_data.json"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

keywords = ['ensemble', 'conformational', 'trajectory', 'dynamics', 'flexibility']

print("Potential Ensemble/Dynamics tools in database:")
count = 0
for tool in data["tools"]:
    usage = tool.get("usage", "") or ""
    strengths = tool.get("strengths", "") or ""
    text = (usage + " " + strengths).lower()
    
    # We ignore fake tools that might match randomly
    if any(k in text for k in keywords) and not tool["id"].endswith("_v") and "v" not in tool["id"]:
        print(f"- {tool['id']} ({tool['category']}): {usage}")
        count += 1

print(f"\nTotal potential tools found: {count}")
