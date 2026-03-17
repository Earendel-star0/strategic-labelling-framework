#!/usr/bin/env python3
"""
Strategic Labelling Framework — NLLE Suggestor v1.0
Automates Rule A (Logic Extraction) by suggesting labels from raw text.
"""

import re
import sys

# Mapping natural language connectives to SLF relops
CONNECTIVES = {
    r'\bif\b.*\bthen\b': '⊢',
    r'\byields\b|\bleads to\b|\bproves\b': '⊢',
    r'\bsame as\b|\bequivalent to\b|\bisomorphic\b': '≅',
    r'\bpart of\b|\binside\b|\bcontained in\b': '⊂',
    r'\band\b|\balso\b': '∧',
    r'\btransforms into\b|\bbecomes\b': '∘'
}

def sanitize_name(text):
    """Converts a phrase into a machine-readable SLF name."""
    clean = re.sub(r'[^A-Za-z0-9\s]', '', text).strip()
    return clean.replace(' ', '_')

def suggest_labels(text):
    """Analyzes text for logical structures and suggests v2.7 labels."""
    suggestions = []
    lines = text.split('.')
    
    for line in lines:
        line = line.strip().lower()
        if not line: continue
        
        for pattern, relop in CONNECTIVES.items():
            match = re.search(pattern, line)
            if match:
                # Heuristic split for subject/object
                parts = re.split(pattern, line, maxsplit=1)
                if len(parts) == 2:
                    subj = sanitize_name(parts[0])
                    obj = sanitize_name(parts[1])
                    
                    if subj and obj:
                        # Suggesting a partial idea with uncertainty per v2.7
                        suggestion = f"~⊕∃f?: {subj} {relop} {obj} ⊣"
                        suggestions.append((line, suggestion))
    
    return suggestions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nlle_suggestor.py \"Your natural language insight here.\"")
        sys.exit(1)
        
    input_text = " ".join(sys.argv[1:])
    results = suggest_labels(input_text)
    
    print(f"--- SLF NLLE: Suggested Propositions (Rule A) ---")
    for raw, suggested in results:
        print(f"\nRaw Text: \"{raw}...\"")
        print(f"Suggested Label: {suggested}")
