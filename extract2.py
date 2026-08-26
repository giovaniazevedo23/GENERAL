import json

paths = [
    r'C:\Users\giova\.gemini\antigravity-ide\brain\5151d71b-d1a9-4f12-88da-497a7b1e18ba\.system_generated\logs\transcript.jsonl',
    r'C:\Users\giova\.gemini\antigravity-ide\brain\5151d71b-d1a9-4f12-88da-497a7b1e18ba\.system_generated\logs\transcript_full.jsonl'
]

for path in paths:
    print(f"Checking {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data.get('tool_calls'):
                    for tc in data['tool_calls']:
                        if tc['name'] in ['replace_file_content', 'multi_replace_file_content']:
                            args = json.dumps(tc['arguments'])
                            if 'index.html' in args:
                                print(f"Found edit in {path}")
                                if 'TargetContent' in args:
                                    print("Found TargetContent")
                                    # Write out the arguments to a file so we can inspect
                                    with open('edit_args.json', 'w', encoding='utf-8') as out:
                                        out.write(args)
    except Exception as e:
        print(f"Error: {e}")
