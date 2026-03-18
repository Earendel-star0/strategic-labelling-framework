#!/usr/bin/env python3
"""
Strategic Labelling Framework — Proof Search v1.1
Automates the 'Epistemic Assembly' of research into a dense crux.
Integrated with Cognitive Linter for automated crux reporting.
"""

import os
import sys
import re
from datetime import datetime

class ProofSearch:
    def __init__(self, corpus_path="research_corpus"):
        self.corpus_path = corpus_path
        self.findings = []

    def gather_witnesses(self, concept, limit=5):
        """Scans the corpus for terms that inhabit the concept."""
        if not os.path.exists(self.corpus_path):
            return
        
        pattern = re.compile(re.escape(concept), re.IGNORECASE)
        
        for root, _, files in os.walk(self.corpus_path):
            for file in files:
                if file.endswith((".md", ".txt", ".log")):
                    self._scan_file(os.path.join(root, file), pattern)
        
        self.findings = self.findings[:limit]

    def _scan_file(self, path, pattern):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = list(pattern.finditer(content))
            for m in matches:
                start = max(0, m.start() - 125)
                end = min(len(content), m.end() + 125)
                snippet = content[start:end].replace('\n', ' ').strip()
                self.findings.append({
                    'source': os.path.relpath(path, self.corpus_path),
                    'witness': f"...{snippet}..."
                })

    def present_crux(self, concept):
        """Standard output for manual research assembly."""
        print(f"\n--- Proof Search: Assembling Witness for '{concept}' ---")
        if not self.findings:
            print(f"  ✗ No witnesses found for '{concept}'.")
            return

        print(f"\n[DENSE CONTEXT: {concept}]")
        print("=" * 60)
        for i, f in enumerate(self.findings, 1):
            print(f"[{i}] SOURCE: {f['source']}\n    {f['witness']}\n")
        print("=" * 60)

def run_for_linter(flagged_items):
    """Integrated hook for tools/cognitive_linter.py."""
    corpus = os.getenv("SLF_CORPUS", "research_corpus")
    engine = ProofSearch(corpus)
    
    report_path = "crux_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# SLF Crux Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("Aggregated research density for items flagged by the Cognitive Linter.\n\n")
        
        for item in flagged_items:
            subj = item['subject']
            f.write(f"## {subj.replace('_', ' ')}\n")
            f.write(f"- **Label**: `{item['label']}`\n")
            f.write(f"- **Prompt**: {item['prompt']}\n\n")
            
            engine.findings = []
            engine.gather_witnesses(subj, limit=3)
            
            if engine.findings:
                f.write("### Assembled Witnesses (Density)\n")
                for i, finding in enumerate(engine.findings, 1):
                    f.write(f"**[{i}] Source: {finding['source']}**\n> {finding['witness']}\n\n")
            else:
                f.write("*No witnesses found in corpus for this concept.*\n\n")
            f.write("---\n\n")
    print(f"--- Proof Search: Integrated report generated at {report_path} ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/proof_search.py <concept_name>")
        sys.exit(1)
    
    target = sys.argv[1]
    ps = ProofSearch(os.getenv("SLF_CORPUS", "research_corpus"))
    ps.gather_witnesses(target)
    ps.present_crux(target)
