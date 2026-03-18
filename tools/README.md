# tools/

Reference toolchain for the Strategic Labelling Framework v2.7.

All tools share a common dependency on `validate_label.py` as their parsing layer. The Cognitive Linter and Journal Manager additionally require `pyyaml` — install via `pip install -r requirements.txt` from the repository root, ideally inside a virtual environment.

---

## Tools Overview

| Tool | Purpose | Dependencies |
| :---- | :---- | :---- |
| `validate_label.py` | Parse and validate labels against the schema | None |
| `linker.py` | Check referential integrity across the repository | `validate_label` |
| `visualizer.py` | Generate a Graphviz DOT graph of the label graph | `validate_label` |
| `nlle_suggestor.py` | Suggest labels from natural language input | None |
| `cognitive_linter.py` | Monitor epistemic velocity across sessions | `validate_label`, `pyyaml` |
| `journal_manager.py` | Write validated session labels to `journal.log` | `validate_label`, `pyyaml` |

---

## validate_label.py

Parses canonical labels against the schema defined in `schema.md`. The foundation of the toolchain — all other tools call it as a library.

### Command line

```bash
python3 tools/validate_label.py "~⊕∃F: My_Concept ⊢ Related_Concept"
python3 tools/validate_label.py "~⊕∃F: My_Concept" --json
```

### Python library

```python
import sys
sys.path.insert(0, 'tools')
from validate_label import validate_label

result = validate_label("~⊕∃F: My_Concept ⊢ Related_Concept")

if result.valid:
    print(f"Subject:     {result.parsed['subject']}")
    print(f"Epistemic:   {result.parsed['epistemic']}")
    print(f"Completeness:{result.parsed['completeness']}")
    print(f"Relations:   {result.parsed['relations']}")
    print(f"Objects:     {result.parsed['objects']}")
else:
    for error in result.errors:
        print(f"✗ {error}")

for warning in result.warnings:
    print(f"⚠ {warning}")
```

### Output (text)

```
Label: ~⊕∃F: My_Concept ⊢ Related_Concept
Status: VALID
Parsed: [~] [⊕] [∃F] : My_Concept
  Relations: ⊢ Related_Concept
```

### Output (JSON)

```json
{
  "label": "~⊕∃F: My_Concept ⊢ Related_Concept",
  "valid": true,
  "errors": [],
  "warnings": [],
  "parsed": {
    "intensity": "~",
    "epistemic": "⊕",
    "completeness": "∃F",
    "project": null,
    "uncertainty": null,
    "subject": "My_Concept",
    "relations": ["⊢"],
    "objects": ["Related_Concept"]
  }
}
```

### Hard errors vs soft warnings

**Hard errors** (label is invalid):
- Missing or invalid intensity marker
- Missing completeness marker
- Invalid subject name (spaces, unsupported characters)
- Unexpected characters in the prefix
- Missing space after colon separator

**Soft warnings** (label is valid, flagged for review):
- Relation present but no object
- More than three relational symbols
- `∄F` label with no description of what is missing

### Test fixtures

```python
FIXTURES = [
    "~∃§: Strategic_Labelling_Framework",
    "!⊕∃F: EGAP-v2.0.1 ⊢ Tensor_Logic",
    "#∃F: Adaptive_Waypoint_System-v1.1",
    "@⊕∃f: Category_Theory ⊂ Protocols",
    "%⊨∃F: App_Scripts · Permission_Reset",
    "~∃F: Epistemic_Node ⊢ Structural_Integrity ∧ Session_Persistence",
    "~⊕∃f: Curry_Howard ⊣",
    "~∴∃F: Category_Theory ⊢ Intersubjective_Communication",
    "~⊕∃f[0.7]: Neural_Manifold ≅ Geometric_Invariant",
    "~∃f?: Speculative_Morphism",
]
```

---

## linker.py

Walks the repository and checks that every object referenced in a relational link exists as a subject somewhere in the label graph. Implements the Linker as specified in `docs/toolchain_specification.md`.

```bash
python3 tools/linker.py .
python3 tools/linker.py path/to/subdir
```

Output:
```
--- SLF Linker: 47 subjects found ---
  ✗ BROKEN: 'Tensor_Logic' in [session_example.md]
--- Status: 1 BROKEN LINKS DETECTED ---
```

---

## visualizer.py

Scans the repository for valid labels and generates a Graphviz DOT file representing the label graph. Derived relations (`∴` epistemic marker) are rendered as dashed blue edges.

```bash
python3 tools/visualizer.py .
dot -Tpng graph.dot -o graph.png
```

`graph.dot` and `graph.png` are excluded from version control via `.gitignore`.

---

## nlle_suggestor.py

Analyses natural language input for logical connectives and suggests preliminary SLF labels. Implements Rule A (Logic Extraction) automation as specified in `docs/toolchain_specification.md`.

Suggested labels are output as `∃f?` — partial and speculative — since they have not been validated by the user.

```bash
python3 tools/nlle_suggestor.py "Proof obligations yield code targets."
python3 tools/nlle_suggestor.py "Category theory is contained in formal methods and also yields protocol design."
```

Output:
```
--- SLF NLLE: Suggested Propositions (Rule A) ---

Raw Text: "proof obligations yield code targets..."
Suggested Label: ~⊕∃f?: Proof_obligations ⊢ Code_targets ⊣
```

---

## journal_manager.py

Appends a validated session label set to `journal.log` in YAML format. The journal is the persistent record of `Γ` across sessions and is the input to the Cognitive Linter.

`journal.log` is excluded from version control via `.gitignore`.

```bash
python3 tools/journal_manager.py
```

### Journal format

```yaml
---
session: 2026-03-18T10:00:00
anchor: "Session description or anchor concept"
protocol: DETENTE
gamma:
  - "~⊕∃F: Curry_Howard_Isomorphism"
  - "#⊕∃F: borrowBook ⊣"
  - "∄F: Void_Type_Clarification — negation semantics undefined"
deferred:
  - subject: "borrowBook"
    reason: "waiting on type system decision"
---
```

`deferred` is optional. Deferred items are acknowledged as open but intentionally parked — the Cognitive Linter treats them with doubled thresholds before re-escalating.

---

## cognitive_linter.py

Reads `journal.log` and monitors epistemic velocity — flagging labels that have stagnated beyond defined session thresholds. Implements the Cognitive Linter as specified in `docs/toolchain_specification.md §2.1`.

```bash
python3 tools/cognitive_linter.py
python3 tools/cognitive_linter.py path/to/journal.log
python3 tools/cognitive_linter.py --json
```

### Thresholds

| Label type | Threshold | Behaviour |
| :---- | :---- | :---- |
| `!∄F` critical blocker | 1 session | `STAGNATION_ALERT` if unresolved |
| `⊣` proof obligation | 3 sessions | Warning if not transitioned |
| `?` heuristic label | 2 sessions | Warning if not formalised |

Deferred items receive doubled thresholds before re-escalating.

### Example output

```
─── SLF Cognitive Linter ─────────────────────────────────────────

⚠  STALE PROOF OBLIGATIONS  (⊣ open past threshold)
   #⊕∃F: borrowBook ⊣
   Sessions open: 4  |  First seen: 2026-03-01
   → "What is the next concrete step toward implementing borrowBook?"

─── Γ Summary ────────────────────────────────────────────────────
   Total tracked:     23
   ∃F+ complete:      18
   ⊣  obligations:    1
   ∄F blockers:       0
   ∃f partials:       2
   Conflict status:   Clear

   Status: 1 issue(s) require attention

   Pass the flagged prompts above into your next session
   to prime blocker resolution before running the audit prompt.
──────────────────────────────────────────────────────────────────
```

### Rule F

The Cognitive Linter also performs temporal Rule F (Conflict Detection) — scanning the full session history for cases where contradictory propositions have been introduced across session boundaries. This catches dissonance that snapshot tools cannot detect.

---

## CI/CD integration

To validate all labels in the repository on every commit:

```yaml
# .github/workflows/validate-labels.yml
name: Validate Labels
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Validate labels
        run: |
          python3 << 'EOF'
          import re, sys
          from pathlib import Path
          sys.path.insert(0, 'tools')
          from validate_label import validate_label

          failed = []
          pattern = r'[!~#@%][∃⊨⊕∴](?:∃F\+|∃F|∃f|∄F|§|⊣)(?:\[[\d.]+\]|\?)?(?:∈\w+)?: \S+'

          for file in Path('.').rglob('*.md'):
              content = file.read_text(encoding='utf-8')
              for label in re.findall(pattern, content):
                  result = validate_label(label)
                  if not result.valid:
                      failed.append((file, label, result.errors))

          if failed:
              for f, l, errs in failed:
                  print(f"✗ {f}: {l}")
                  for e in errs: print(f"  {e}")
              sys.exit(1)

          print("✓ All labels valid")
          EOF
```

---

**See also:**
- `schema.md` — formal grammar and canonical rules
- `docs/toolchain_specification.md` — design specification for all tools
- `examples/audit_prompt.md` — v2.7 canonical audit prompt
- `PHILOSOPHY.md` — why epistemic honesty matters
