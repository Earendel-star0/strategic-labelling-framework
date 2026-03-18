#!/usr/bin/env python3
"""
Strategic Labelling Framework — Proof Search v1.0
Automates the 'Epistemic Assembly' of research into a dense crux.
"""

import os
import sys
import re

class ProofSearch:
    def __init__(self, corpus_path="research_corpus"):
        """
        Initializes the search engine. 
        'corpus_path' should point to the directory containing your research.
        """
        self.corpus_path = corpus_path
        self.findings = []

    def gather_witnesses(self, concept, limit=5):
        """
        Scans the corpus for terms (snippets) that inhabit the concept.
        This is the 'Proof Search' in the Curry-Howard sense.
        """
        if not os.path.exists(self.corpus_path):
            print(f"--- Warning: Corpus directory '{self.corpus_path}' not found ---")
            print(f"--- Create the directory and add your research files to begin. ---")
            return
        
        # Search for the concept (case-insensitive)
        pattern = re.compile(re.escape(concept), re.IGNORECASE)
        
        for root, _, files in os.walk(self.corpus_path):
            for file in files:
                if file.endswith((".md", ".txt", ".log")):
                    self._scan_file(os.path.join(root, file), pattern)
        
        # Sort or filter findings if necessary (currently returns first N matches)
        self.findings = self.findings[:limit]

    def _scan_file(self, path, pattern):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = list(pattern.finditer(content))
            for m in matches:
                # Extract 250 characters of context around the match
                start = max(0, m.start() - 125)
                end = min(len(content), m.end() + 125)
                snippet = content[start:end].replace('\n', ' ').strip()
                self.findings.append({
                    'source': os.path.relpath(path, self.corpus_path),
                    'witness': f"...{snippet}..."
                })

    def present_crux(self, concept):
        """Presents the assembled density for unencumbered dialogue."""
        print(f"\n--- Proof Search: Assembling Witness for '{concept}' ---")
        if not self.findings:
            print(f"  ✗ No witnesses found for '{concept}' in the current corpus.")
            return

        print(f"\n[DENSE CONTEXT: {concept}]")
        print("=" * 60)
        for i, f in enumerate(self.findings, 1):
            print(f"[{i}] SOURCE: {f['source']}")
            print(f"    {f['witness']}\n")
        print("=" * 60)
        print("--- Status: Crux Assembled. Transition to Unencumbered Dialogue recommended. ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/proof_search.py <concept_name>")
        sys.exit(1)
    
    target_concept = sys.argv[1]
    # Default to 'research_corpus' folder; can be overridden via environment variable
    corpus = os.getenv("SLF_CORPUS", "research_corpus")
    
    engine = ProofSearch(corpus)
    engine.gather_witnesses(target_concept)
    engine.present_crux(target_concept)
