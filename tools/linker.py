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
