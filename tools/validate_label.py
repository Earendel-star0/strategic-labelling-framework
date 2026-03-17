#!/usr/bin/env python3
"""
Strategic Labelling Framework — Label Validator

Validates labels against the canonical schema defined in schema.md.
Emits hard errors (label is invalid) and soft warnings (label is valid but flagged for review).

Usage:
    python validate_label.py "~∃F: My_Concept"
    python validate_label.py "~∃F: My_Concept ⊢ Other_Concept" --json
    from validate_label import validate_label; result = validate_label("~∃F: My_Concept")
"""

import re
import sys
import json
from typing import Dict, List, Tuple

# Valid marker sets
INTENSITY = {'!', '~', '#', '@', '%'}
EPISTEMIC = {'∃', '⊨', '⊕', '∴'}
COMPLETENESS = {'∃F+', '∃F', '∃f', '∄F', '§', '⊣'}
RELATIONAL = {'∈', '⊂', '⊢', '≅', '∘', '∧', '·', '↳', '⊣'}

# Regex patterns
WORD_PATTERN = r'[A-Za-z0-9]+'
NAME_PATTERN = r'[A-Za-z0-9]+(?:[_\-\.][A-Za-z0-9]+)*'  # Allow _, -, . as separators
INTENSITY_PATTERN = r'[!~#@%]'
EPISTEMIC_PATTERN = r'[∃⊨⊕∴]'
COMPLETENESS_PATTERN = r'∃F\+|∃F|∃f|∄F|§|⊣'
RELATIONAL_PATTERN = r'[∈⊂⊢≅∘∧·↳⊣]'


class ValidationResult:
    def __init__(self, label: str):
        self.label = label
        self.valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.parsed = {
            'intensity': None,
            'epistemic': None,
            'completeness': None,
            'project': None,
            'subject': None,
            'relations': [],
            'objects': []
        }

    def add_error(self, msg: str):
        self.valid = False
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def to_dict(self):
        return {
            'label': self.label,
            'valid': self.valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'parsed': self.parsed if self.valid else None
        }

    def __str__(self):
        lines = [f"Label: {self.label}"]
        if self.valid:
            lines.append("Status: VALID")
        else:
            lines.append("Status: INVALID")
        
        if self.errors:
            lines.append("Errors:")
            for err in self.errors:
                lines.append(f"  ✗ {err}")
        
        if self.warnings:
            lines.append("Warnings:")
            for warn in self.warnings:
                lines.append(f"  ⚠ {warn}")
        
        if self.valid and self.parsed['subject']:
            lines.append(f"Parsed: [{self.parsed['intensity']}] [{self.parsed['epistemic']}] [{self.parsed['completeness']}] : {self.parsed['subject']}")
            if self.parsed['relations']:
                rels = " ".join(f"{r} {o}" if o else r for r, o in zip(self.parsed['relations'], self.parsed['objects']))
                lines.append(f"  Relations: {rels}")
        
        return "\n".join(lines)


def validate_label(label: str) -> ValidationResult:
    """
    Validate a single label against the schema.
    
    Correct interpretation:
    [Intensity][Epistemic?][Completeness] : [Subject] [Relation Object]*
    
    Where:
    - Intensity: !, ~, #, @, %
    - Epistemic: ⊨, ⊕, ∴ (OR implicitly ∃ if completeness starts with ∃)
    - Completeness: ∃F+, ∃F, ∃f, ∄F, §, ⊣
    
    Examples:
    - ~∃F: ... (intensity=~, epistemic=∃ [implicit], completeness=∃F)
    - ~⊕∃F: ... (intensity=~, epistemic=⊕, completeness=∃F)
    - !⊨∃F+: ... (intensity=!, epistemic=⊨, completeness=∃F+)
    """
    result = ValidationResult(label)
    label = label.strip()
    
    if not label:
        result.add_error("Label is empty")
        return result
    
    # Check for colon separator
    if ':' not in label:
        result.add_error("Missing colon separator — expected format: [Intensity][Epistemic][Completeness] : [Subject]")
        return result
    
    # Split on colon
    parts = label.split(':', 1)
    if len(parts) != 2:
        result.add_error("Multiple colons found — only one separator allowed")
        return result
    
    prefix, suffix = parts
    
    # Validate whitespace around colon
    if suffix and suffix[0] != ' ':
        result.add_error("Missing space after colon separator")
        return result
    
    suffix = suffix.lstrip()  # Remove leading space(s)
    
    # Parse prefix (intensity, epistemic, completeness, project)
    idx = 0
    
    # 1. Intensity marker (required, exactly one)
    if idx >= len(prefix):
        result.add_error("Missing intensity marker")
        return result
    
    if prefix[idx] not in INTENSITY:
        result.add_error(f"Invalid intensity marker '{prefix[idx]}' — must be one of: ! ~ # @ %")
        return result
    
    result.parsed['intensity'] = prefix[idx]
    idx += 1
    
    # 2. Epistemic marker (can be implicit ∃ or explicit ⊨, ⊕, ∴)
    # Try to match explicit epistemic markers first
    epistemic_found = False
    if idx < len(prefix) and prefix[idx] in {'⊨', '⊕', '∴'}:
        result.parsed['epistemic'] = prefix[idx]
        idx += 1
        epistemic_found = True
    
    # 3. Completeness marker (required, exactly one) — handle ∃F+ first
    remaining = prefix[idx:]
    comp = None
    comp_len = 0
    
    # Match in order of length to avoid ∃F matching when ∃F+ is intended
    if remaining.startswith('∃F+'):
        comp = '∃F+'
        comp_len = 3
    elif remaining.startswith('∃F'):
        comp = '∃F'
        comp_len = 2
    elif remaining.startswith('∃f'):
        comp = '∃f'
        comp_len = 2
    elif remaining.startswith('∄F'):
        comp = '∄F'
        comp_len = 2
    elif remaining.startswith('§'):
        comp = '§'
        comp_len = 1
    elif remaining.startswith('⊣'):
        comp = '⊣'
        comp_len = 1
    else:
        result.add_error(f"Invalid completeness marker — must be one of: ∃F+ ∃F ∃f ∄F § ⊣")
        return result
    
    # If completeness starts with ∃ and no explicit epistemic was found, ∃ is implicit epistemic
    if comp and comp[0] == '∃' and not epistemic_found:
        result.parsed['epistemic'] = '∃'
    elif not epistemic_found and comp and comp[0] != '∃':
        result.add_error("Missing epistemic marker — must be one of: ∃ ⊨ ⊕ ∴")
        return result
    
    result.parsed['completeness'] = comp
    idx += comp_len
    
    # 4. Project membership (optional) — ∈ProjectName
    if idx < len(prefix) and prefix[idx] == '∈':
        idx += 1
        proj_match = re.match(r'^' + NAME_PATTERN, prefix[idx:])
        if proj_match:
            result.parsed['project'] = proj_match.group(0)
            idx += len(proj_match.group(0))
        else:
            result.add_warning("Project membership marker (∈) present but no valid project name follows")
    
    # Check for leftover characters in prefix
    if idx < len(prefix):
        result.add_error(f"Unexpected characters after markers: '{prefix[idx:]}'")
        return result
    
    # Parse suffix (subject, relations, objects)
    parts = suffix.split()
    if not parts:
        result.add_error("Missing subject after colon")
        return result
    
    # First part is the subject
    subject = parts[0]
    
    # Validate subject name
    if not re.match(r'^' + NAME_PATTERN + r'$', subject):
        if ' ' in subject:
            result.add_warning("Subject contains spaces — use underscore for multi-word names")
        else:
            result.add_error(f"Invalid subject name: '{subject}' — must be alphanumeric with underscores/hyphens only")
            return result
    
    result.parsed['subject'] = subject
    
    # Parse relations and objects
    relation_parts = parts[1:] if len(parts) > 1 else []
    relations = []
    objects = []
    i = 0
    
    while i < len(relation_parts):
        part = relation_parts[i]
        
        # Check if it's a relational operator
        if len(part) == 1 and part in RELATIONAL:
            relations.append(part)
            # Next part (if present) is the object
            if i + 1 < len(relation_parts):
                obj_candidate = relation_parts[i + 1]
                if obj_candidate[0] not in RELATIONAL and re.match(r'^' + NAME_PATTERN + r'$', obj_candidate):
                    objects.append(obj_candidate)
                    i += 2
                else:
                    # Relation without object is allowed but flagged
                    objects.append(None)
                    i += 1
            else:
                # Relation at end with no object
                objects.append(None)
                i += 1
        else:
            result.add_warning(f"Unexpected token in relations: '{part}' — expected relational operator")
            i += 1
    
    if len(relations) > len(objects):
        objects.extend([None] * (len(relations) - len(objects)))
    
    result.parsed['relations'] = relations
    result.parsed['objects'] = objects
    
    # Soft warnings
    if len(relations) > 3:
        result.add_warning(f"Maximum three relations per label exceeded ({len(relations)} found)")
    
    for rel, obj in zip(relations, objects):
        if rel and not obj:
            result.add_warning(f"Relation '{rel}' has no object — consider completing")
    
    if result.parsed['completeness'] == '∄F' and not any(w in result.label for w in ['—', ':', 'description']):
        result.add_warning("∄F blocker label should include a description of what is missing")
    
    return result


def validate_batch(labels: List[str], verbose: bool = False) -> List[ValidationResult]:
    """Validate multiple labels and return results."""
    results = [validate_label(label) for label in labels]
    
    if verbose:
        for result in results:
            print(result)
            print()
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_label.py <label> [--json]")
        print("Example: python validate_label.py '~∃F: My_Concept'")
        sys.exit(1)
    
    label = sys.argv[1]
    output_json = '--json' in sys.argv
    
    result = validate_label(label)
    
    if output_json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(result)
    
    sys.exit(0 if result.valid else 1)
