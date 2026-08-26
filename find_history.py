import json

log_file = r'C:\Users\giova\.gemini\antigravity-ide\brain\1f87a778-79b5-44af-8e10-9e76c9507dac\.system_generated\logs\transcript_full.jsonl'
best_step = -1
content = ""

try:
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            step = json.loads(line)
            # Search all strings in the JSON for the content of index.html
            line_str = json.dumps(step)
            if '<!DOCTYPE html>' in line_str and '<html lang="pt-BR">' in line_str and 'GENERAL App' in line_str:
                if 'tool_calls' in step:
                    for tc in step['tool_calls']:
                        if 'index.html' in str(tc):
                            # Check if this is the original write_to_file or multi_replace
                            args = tc.get('args', {}) or tc.get('function', {}).get('arguments', {})
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except: pass
                            
                            if isinstance(args, dict):
                                code = args.get('CodeContent', '')
                                if not code and 'ReplacementChunks' in args:
                                    # It's an edit, we want the LAST FULL write_to_file
                                    pass
                                elif code:
                                    best_step = step['step_index']
                                    content = code
except Exception as e:
    print('Error:', e)

if best_step != -1:
    print(f"Found original index.html at step {best_step}!")
    with open('index_recovered.html', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find full index.html in logs.")
