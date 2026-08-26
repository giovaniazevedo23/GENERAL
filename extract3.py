import json

path = r'C:\Users\giova\.gemini\antigravity-ide\brain\5151d71b-d1a9-4f12-88da-497a7b1e18ba\.system_generated\logs\transcript_full.jsonl'
print(f"Checking {path}")
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('tool_calls'):
            for tc in data['tool_calls']:
                if tc.get('name') in ['replace_file_content', 'multi_replace_file_content']:
                    # The arguments might be in tc['args'] or tc['arguments']
                    args = tc.get('arguments', tc.get('args', {}))
                    args_str = json.dumps(args)
                    if 'index.html' in args_str:
                        print(f"Found edit in {path}")
                        with open('edit_args.json', 'a', encoding='utf-8') as out:
                            out.write(args_str + "\n")
