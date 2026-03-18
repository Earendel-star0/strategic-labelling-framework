# Quick Start — Strategic Labelling Framework v2.7

Get up and running in 5 minutes.

---

## What the Framework Does

The SLF gives every idea a label that records three things: how confident you are in it, where it came from, and how complete it is. Over time, the label graph becomes a map of how your thinking has moved — one that persists across sessions and can be reasoned over by the toolchain.

---

## The Label Structure

```
[Intensity] [Epistemic] [Completeness] [Project∈] [Uncertainty] : [Subject] [Relation] [Object]
```

A minimal valid label:

```
~∃F: My_Concept
```

A full label:

```
!⊕∃F∈SLF[0.9]: Cognitive_Linter ⊢ Epistemic_Velocity
```

Read left to right: powerful insight, co-instantiated with AI, well-formed, belongs to SLF project, 90% confidence — Cognitive_Linter yields Epistemic_Velocity.

---

## Markers at a Glance

```
Intensity:    !  ~  #  @  %
Epistemic:    ∃  ⊨  ⊕  ∴
Completeness: ∃F+  ∃F  ∃f  ∄F  §  ⊣
Uncertainty:  [0.0–1.0]  ?
Relations:    ∈  ⊂  ⊢  ≅  ∘  ∧  ·  ↳  ⊣   (max 3)
```

---

## Validating a Label

### Command line

```bash
cd ~/strategic-labelling-framework
python3 tools/validate_label.py "~∃F: My_Concept"
```

Output:
```
Label: ~∃F: My_Concept
Status: VALID
Parsed: [~] [∃] [∃F] : My_Concept
```

### In Python

```python
import sys
sys.path.insert(0, 'tools')
from validate_label import validate_label

result = validate_label("~⊕∃F: My_Concept ⊢ Related_Concept")

if result.valid:
    print(f"Subject:    {result.parsed['subject']}")
    print(f"Epistemic:  {result.parsed['epistemic']}")
    print(f"Relations:  {result.parsed['relations']}")
else:
    for error in result.errors:
        print(f"✗ {error}")
```

---

## Common Patterns

### A well-formed idea

```
~∃F: Strategic_Labelling_Framework
```

### A co-instantiated idea with a relation

```
~⊕∃F: Four_Stage_Pipeline ⊢ Code_Generation
```

### A proof obligation (typed but unimplemented)

```
#⊕∃F: borrowBook ⊣
```

### A versioned idea

```
~⊕∃F: Attention_Mechanism-v2.1 ⊢ Query_Key_Scaling-v1.0
```

### A speculative idea

```
~∃f?: Speculative_Morphism
```

### A derived idea (Rule D)

```
~∴∃F: Category_Theory ⊢ Intersubjective_Communication
```

---

## What the Validator Checks

**Hard errors** (label rejected):
- ✗ Missing intensity marker: `∃F: Concept`
- ✗ Invalid subject name: `~∃F: My Concept` (use underscore)
- ✗ Missing space after colon: `~∃F:Concept`
- ✗ Invalid completeness marker

**Soft warnings** (label accepted, flagged for review):
- ⚠ Relation without object: `~∃F: Concept ⊢`
- ⚠ More than three relations
- ⚠ `∄F` with no description of what is missing

---

## Running the Toolchain

All tools live in `tools/` and are run from the repository root. The Cognitive Linter and Journal Manager require the virtual environment (`pyyaml` dependency).

```bash
# Activate the virtual environment
source .venv/bin/activate

# Validate a label
python3 tools/validate_label.py "~⊕∃F: My_Concept"

# Check all relational links across the repository
python3 tools/linker.py .

# Generate a graph visualisation
python3 tools/visualizer.py .
dot -Tpng graph.dot -o graph.png

# Suggest labels from natural language
python3 tools/nlle_suggestor.py "Proof obligations yield code targets."

# Write a session to the journal
python3 tools/journal_manager.py

# Run the cognitive linter
python3 tools/cognitive_linter.py
```

---

## The Session Workflow

```
1. Work in a session — develop ideas, write code, do research
        ↓
2. Run the audit prompt (examples/audit_prompt.md)
   — Claude labels all ideas, checks readiness, fires Rules D/E/F
        ↓
3. Run the labelling prompt (examples/labelling_prompt.md)
   — Claude produces the final validated label set
        ↓
4. Journal the session
   python3 tools/journal_manager.py
        ↓
5. Run the cognitive linter before the next session
   python3 tools/cognitive_linter.py
   — flags stale obligations and unresolved blockers
        ↓
6. Repeat
```

---

## Troubleshooting

**"Invalid subject name"**
Use underscores for multi-word names (`My_Concept`), hyphens for versioning (`Algorithm-v2.0`), dots for version components (`v2.0.1`). No spaces.

**"Missing space after colon"**
The separator is ` : ` — one space each side. `~∃F: Concept` is correct. `~∃F:Concept` is not.

**"Relation has no object" warning**
This is a soft warning, not an error. The label is valid but flagged. Complete it: `Concept ⊢ Related_Concept`.

**"Invalid completeness marker"**
Must be exactly one of: `∃F+`, `∃F`, `∃f`, `∄F`, `§`, `⊣`. Note `∃F+` must be written before `∃F` is matched — the validator handles this, but be precise when writing manually.

**Cognitive Linter can't find journal.log**
Run `python3 tools/journal_manager.py` first to create the journal, then re-run the linter.

---

## Schema Reference

Full formal grammar is in `schema.md`. The BNF in brief:

```
label        ::= intensity epistemic completeness [project] [uncertainty] ":" SPACE subject [relations]
name         ::= word (("_" | "-" | ".") word)*
word         ::= [A-Za-z0-9]+
uncertainty  ::= "[" float "]" | "?"
float        ::= "0." [0-9]+ | "1.0"
```

---

## Files in This Repository

```
schema.md                        ← formal grammar (canonical reference)
strategic_labelling_framework.md ← full layer reference with examples
PHILOSOPHY.md                    ← why the framework exists
CHANGELOG.md                     ← version history
extensions/
  curry_howard_extension.md      ← Curry-Howard correspondence and ⊣
  operational_semantics.md       ← Rules A–F and the Epistemic Environment
  rule_d_primer.md               ← Rule D in depth
docs/
  rule_d_implications.md         ← generative implications of Rule D
  toolchain_specification.md     ← toolchain design specification
examples/
  audit_prompt.md                ← v2.7 canonical audit prompt
  labelling_prompt.md            ← session labelling prompt
  session_example.md             ← annotated worked example
tools/
  validate_label.py              ← label validator
  linker.py                      ← cross-file link checker
  visualizer.py                  ← graph generator
  nlle_suggestor.py              ← natural language label suggester
  cognitive_linter.py            ← epistemic velocity monitor
  journal_manager.py             ← session journal writer
```
