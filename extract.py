import json

with open(r'C:\Users\giova\.gemini\antigravity-ide\brain\5151d71b-d1a9-4f12-88da-497a7b1e18ba\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('tool_calls'):
            for tc in data['tool_calls']:
                if tc['name'] in ['replace_file_content', 'multi_replace_file_content']:
                    try:
                        args = tc['arguments']
                        if 'index.html' in args:
                            print(f"Tool: {tc['name']}")
                            print(f"Args: {args[:500]}...") # truncate so we just see what happened
                    except:
                        pass
