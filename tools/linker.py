#!/usr/bin/env python3
"""
Strategic Labelling Framework — The Linker v1.0
Implements cross-file relational resolution for the v2.7 specification.
"""

import os
import re
import sys
from typing import Dict, Set, List
from validate_label import validate_label # Uses the v2.7 validator

class SLFLinker:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.subjects: Dict[str, str] = {} # subject -> filename
        self.references: List[tuple] = [] # (object, source_label, filename)
        self.errors: List[str] = []

    def scan_repository(self):
        """Walks the repo and parses all .md files for labels."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    self._parse_file(os.path.join(root, file))

    def _parse_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Look for the SLF colon separator
                if ':' in line:
                    result = validate_label(line.strip())
                    if result.valid:
                        subj = result.parsed['subject']
                        self.subjects[subj] = os.path.basename(filepath)
                        
                        # Collect all objects referenced in relations
                        for obj in result.parsed['objects']:
                            if obj:
                                self.references.append((obj, line.strip(), os.path.basename(filepath)))

    def resolve_links(self):
        """Checks if every referenced object exists as a subject."""
        print(f"--- SLF Linker: Resolving Γ across {len(self.subjects)} subjects ---")
        
        for obj, source_label, source_file in self.references:
            if obj not in self.subjects:
                msg = f"BROKEN LINK: '{obj}' referenced in [{source_file}] but never defined."
                print(f"  ✗ {msg}")
                print(f"    Label: {source_label}")
                self.errors.append(msg)
            else:
                # Optional: Trace Rule D Transitivity
                pass

        if not self.errors:
            print("--- Status: ALL LINKS RESOLVED (Structural Syntropy Confirmed) ---")
        else:
            print(f"--- Status: {len(self.errors)} BROKEN LINKS DETECTED ---")

if __name__ == "__main__":
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    linker = SLFLinker(repo_root)
    linker.scan_repository()
    linker.resolve_links()
    sys.exit(0 if not linker.errors else 1)
