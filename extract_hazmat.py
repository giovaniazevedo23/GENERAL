import json

path = r'C:\Users\giova\.gemini\antigravity-ide\brain\5151d71b-d1a9-4f12-88da-497a7b1e18ba\.system_generated\logs\transcript_full.jsonl'
print(f"Checking {path}")
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        # Look at the tool response content
        if data.get('type') == 'TOOL_RESPONSE' and data.get('content'):
            if 'id="view-hazmat"' in data['content']:
                with open('hazmat_found.txt', 'a', encoding='utf-8') as out:
                    out.write(data['content'] + "\n\n=====\n\n")
