#!/usr/bin/env python3
import os, sys
from validate_label import validate_label

class SLFVisualizer:
    def __init__(self):
        self.nodes = {} # dict mapping node -> completeness
        self.edges = [] 

    def scan_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    res = validate_label(line.strip())
                    if res.valid:
                        subj = res.parsed['subject']
                        comp = res.parsed['completeness']
                        is_derived = res.parsed['epistemic'] == '∴'
                        
                        # Upgrade completeness state if discovered
                        if subj not in self.nodes or comp in ['∃F+', '∃F', '§']:
                            self.nodes[subj] = comp
                            
                        for rel, obj in zip(res.parsed['relations'], res.parsed['objects']):
                            if obj:
                                if obj not in self.nodes:
                                    self.nodes[obj] = 'UNKNOWN'
                                self.edges.append((subj, obj, rel, is_derived))

    def generate_dot(self, output_path: str):
        colors = {
            '∃F+': 'darkgreen', '∃F': 'black', '∃f': 'gray', 
            '∄F': 'red', '⊣': 'darkorange', '§': 'purple', 'UNKNOWN': 'lightgray'
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("digraph SLF_Graph {\n")
            f.write("  rankdir=LR;\n")
            f.write("  node [shape=box, style=filled, fillcolor=white, fontname=\"Arial\"];\n\n")

            # Apply completeness coloring
            for node, comp in self.nodes.items():
                col = colors.get(comp, 'black')
                f.write(f"  \"{node}\" [color=\"{col}\", fontcolor=\"{col}\", penwidth=2];\n")

            f.write("\n")

            for subj, obj, rel, derived in self.edges:
                style = " [label=\" " + rel + " \", color=blue, fontcolor=blue, style=dashed]" if derived else f" [label=\" {rel} \"]"
                f.write(f"  \"{subj}\" -> \"{obj}\"{style};\n")

            f.write("}\n")
        print(f"--- Visualizer: DOT file generated at {output_path} ---")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    viz = SLFVisualizer()
    for root, _, files in os.walk(target):
        for file in files:
            if file.endswith(".md"):
                viz.scan_file(os.path.join(root, file))
    viz.generate_dot("graph.dot")
