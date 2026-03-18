#!/bin/bash
# Strategic Labelling Framework — Unified Toolchain Installer v2.8-alpha

echo "--- Initializing SLF v2.8-alpha Toolchain ---"

# 1. Create tools directory if it doesn't exist
mkdir -p tools

# 2. Update Validator (v2.7 Logic)
cat << 'PY' > tools/validate_label.py
import re, sys, json
INTENSITY = {'!', '~', '#', '@', '%'}
EPISTEMIC = {'∃', '⊨', '⊕', '∴'}
COMPLETENESS = {'∃F+', '∃F', '∃f', '∄F', '§', '⊣'}
RELATIONAL = {'∈', '⊂', '⊢', '≅', '∘', '∧', '·', '↳', '⊣'}
NAME_PATTERN = r'[A-Za-z0-9]+(?:[_\-\.][A-Za-z0-9]+)*'
UNCERTAINTY = r'(\[(\d\.\d|1\.0)\]|\?)'

def validate_label(label):
    class Result:
        def __init__(self, l): self.label, self.valid, self.errors, self.warnings, self.parsed = l, True, [], [], {'intensity':None,'epistemic':None,'completeness':None,'project':None,'uncertainty':None,'subject':None,'relations':[],'objects':[]}
        def to_dict(self): return {'label':self.label,'valid':self.valid,'errors':self.errors,'warnings':self.warnings,'parsed':self.parsed if self.valid else None}
    
    res = Result(label.strip())
    if ':' not in res.label: res.errors.append("Missing colon"); res.valid=False; return res
    prefix, suffix = res.label.split(':', 1)
    if suffix and suffix[0] != ' ': res.errors.append("Missing space after colon"); res.valid=False; return res
    suffix = suffix.lstrip(); idx = 0
    if not prefix or prefix[0] not in INTENSITY: res.errors.append("Invalid intensity"); res.valid=False; return res
    res.parsed['intensity'] = prefix[0]; idx += 1
    if idx < len(prefix) and prefix[idx] in {'⊨', '⊕', '∴'}: res.parsed['epistemic'] = prefix[idx]; idx += 1
    rem = prefix[idx:]
    comp_map = {'∃F+':3,'∃F':2,'∃f':2,'∄F':2,'§':1,'⊣':1}
    found_comp = next((c for c in comp_map if rem.startswith(c)), None)
    if not found_comp: res.errors.append("Invalid completeness"); res.valid=False; return res
    if found_comp.startswith('∃') and not res.parsed['epistemic']: res.parsed['epistemic'] = '∃'
    res.parsed['completeness'] = found_comp; idx += comp_map[found_comp]
    if idx < len(prefix) and prefix[idx] == '∈':
        idx += 1; m = re.match(r'^' + NAME_PATTERN, prefix[idx:])
        if m: res.parsed['project'] = m.group(0); idx += len(m.group(0))
    if idx < len(prefix):
        m = re.match(r'^' + UNCERTAINTY, prefix[idx:])
        if m: res.parsed['uncertainty'] = m.group(0); idx += len(m.group(0))
    if idx < len(prefix): res.errors.append(f"Unexpected: {prefix[idx:]}"); res.valid=False; return res
    parts = suffix.split()
    if not parts: res.errors.append("Missing subject"); res.valid=False; return res
    if not re.match(r'^' + NAME_PATTERN + r'$', parts[0]): res.errors.append(f"Invalid subject: {parts[0]}"); res.valid=False; return res
    res.parsed['subject'] = parts[0]
    rel_parts = parts[1:]; i = 0
    while i < len(rel_parts):
        p = rel_parts[i]
        if len(p) == 1 and p in RELATIONAL:
            res.parsed['relations'].append(p)
            if i+1 < len(rel_parts) and re.match(r'^' + NAME_PATTERN + r'$', rel_parts[i+1]):
                res.parsed['objects'].append(rel_parts[i+1]); i += 2
            else: res.parsed['objects'].append(None); res.warnings.append(f"Relation {p} missing object"); i += 1
        else: res.warnings.append(f"Unexpected token: {p}"); i += 1
    return res

if __name__ == "__main__":
    if len(sys.argv) > 1:
        r = validate_label(sys.argv[1])
        if '--json' in sys.argv: print(json.dumps(r.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(f"Label: {r.label}\nStatus: {'VALID' if r.valid else 'INVALID'}")
            for e in r.errors: print(f"  ✗ {e}")
            for w in r.warnings: print(f"  ⚠ {w}")
PY

# 3. Create Linker
cat << 'PY' > tools/linker.py
import os, sys
from validate_label import validate_label
class SLFLinker:
    def __init__(self, root): self.root, self.subjects, self.references, self.errors = root, {}, [], []
    def run(self):
        for r, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".md"):
                    with open(os.path.join(r, f), 'r') as file:
                        for line in file:
                            if ':' in line:
                                res = validate_label(line.strip())
                                if res.valid:
                                    self.subjects[res.parsed['subject']] = f
                                    for o in res.parsed['objects']:
                                        if o: self.references.append((o, line.strip(), f))
        print(f"--- SLF Linker: {len(self.subjects)} subjects found ---")
        for o, l, f in self.references:
            if o not in self.subjects: print(f"  ✗ BROKEN: '{o}' in [{f}]"); self.errors.append(o)
        if not self.errors: print("--- Status: ALL LINKS RESOLVED ---")
if __name__ == "__main__": SLFLinker(".").run()
PY

# 4. Create Journal Manager
cat << 'PY' > tools/journal_manager.py
import datetime, yaml, os
from validate_label import validate_label
class JournalManager:
    def append(self, gamma, anchor="None", protocol="DETENTE"):
        entry = {'session': datetime.datetime.now().isoformat(), 'anchor': anchor, 'protocol': protocol, 'gamma': [l for l in gamma if validate_label(l).valid]}
        with open("journal.log", 'a') as f: f.write("---\n"); yaml.dump(entry, f)
        print(f"--- Journaled {len(entry['gamma'])} labels ---")
if __name__ == "__main__": JournalManager().append(["!⊕∃F+: Virtual_Environment ⊢ Tool_Isolation"], anchor="Setup")
PY

# 5. Create requirements.txt
echo "pyyaml==6.0.1" > requirements.txt

# 6. Finalize permissions
chmod +x tools/*.py
echo "--- v2.8-alpha Toolchain Materialized ---"
