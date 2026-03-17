#!/usr/bin/env python3
"""
Strategic Labelling Framework — The Visualizer v1.0
Generates Graphviz DOT files from SLF v2.7 label graphs.
"""

import os
import sys
from validate_label import validate_label

class SLFVisualizer:
    def __init__(self):
        self.nodes = set()
        self.edges = [] # List of (subj, obj, relation_type, is_derived)

    def scan_file(self, filepath: str):
        """Parses a file for labels and builds the graph structure."""
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    res = validate_label(line.strip())
                    if res.valid:
                        subj = res.parsed['subject']
                        is_derived = res.parsed['epistemic'] == '∴'
                        self.nodes.add(subj)
                        
                        for rel, obj in zip(res.parsed['relations'], res.parsed['objects']):
                            if obj:
                                self.nodes.add(obj)
                                self.edges.append((subj, obj, rel, is_derived))

    def generate_dot(self, output_path: str):
        """Outputs a DOT file for rendering with Graphviz."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("digraph SLF_Graph {\n")
            f.write("  rankdir=LR;\n")
            f.write("  node [shape=box, style=filled, fillcolor=white, fontname=\"Arial\"];\n\n")

            # Style derived nodes differently
            for node in self.nodes:
                f.write(f"  \"{node}\";\n")

            f.write("\n")

            for subj, obj, rel, derived in self.edges:
                style = " [label=\" " + rel + " \", color=blue, fontcolor=blue, style=dashed]" if derived else f" [label=\" {rel} \"]"
                f.write(f"  \"{subj}\" -> \"{obj}\"{style};\n")

            f.write("}\n")
        print(f"--- Visualizer: DOT file generated at {output_path} ---")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    viz = SLFVisualizer()
    
    if os.path.isfile(target):
        viz.scan_file(target)
    else:
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(".md"):
                    viz.scan_file(os.path.join(root, file))

    viz.generate_dot("graph.dot")
