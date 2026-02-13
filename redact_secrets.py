import json
import os
import re

def redact_secrets(path):
    if not os.path.exists(path):
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            print(f"Skipping {path}: Invalid JSON")
            return
    
    changed = False
    # Pattern for Hugging Face tokens
    hf_pattern = re.compile(r'hf_[a-zA-Z0-9]{34}')
    
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                new_line = hf_pattern.sub('HF_TOKEN_REDACTED', line)
                if new_line != line:
                    changed = True
                new_source.append(new_line)
            cell['source'] = new_source
            
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Redacted secrets in {path}")

if __name__ == "__main__":
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb"):
                redact_secrets(os.path.join(root, file))
