# Integration Guide — Using the Refinements

This document shows how the three refinements work together in real workflows.

---

## Scenario 1: AI-Assisted Label Generation in a Session

Richard is in an active session with Claude. They've built several ideas and want to label them before moving to the implementation stage.

### Step 1: Audit the session (existing workflow)

Richard gives Claude the audit prompt from `examples/audit_prompt.md`. Claude generates a label set:

```
~∃F: Curry_Howard_Isomorphism
~⊕∃F: Type_Signature_Generation ⊣
#⊕∃F: borrowBook ⊣
∄F: Void_Type_Clarification — missing definition of negation semantics
```

### Step 2: Validate the labels (new workflow)

Before returning, Claude runs each label through the validator:

```python
from validate_label import validate_label

labels = [
    "~∃F: Curry_Howard_Isomorphism",
    "~⊕∃F: Type_Signature_Generation ⊣",
    "#⊕∃F: borrowBook ⊣",
    "∄F: Void_Type_Clarification",
]

all_valid = True
for label in labels:
    result = validate_label(label)
    if not result.valid:
        print(f"✗ Invalid: {label}")
        for error in result.errors:
            print(f"  {error}")
        all_valid = False
    else:
        print(f"✓ Valid: {label}")

if not all_valid:
    # Regenerate and re-validate
    pass
```

**Output:**
```
✓ Valid: ~∃F: Curry_Howard_Isomorphism
✓ Valid: ~⊕∃F: Type_Signature_Generation ⊣
✓ Valid: #⊕∃F: borrowBook ⊣
✓ Valid: ∄F: Void_Type_Clarification
```

Claude returns the validated label set to Richard with confidence that it conforms to the schema.

### Step 3: Move to blocker resolution

Richard sees the `∄F` item. Using the narrowed-down blocker, he clarifies the negation semantics, which Claude captures as:

```
#⊕∃F: Negation_Mapping ⊂ Connective_Mapping
```

Claude validates this new label:
```python
result = validate_label("#⊕∃F: Negation_Mapping ⊂ Connective_Mapping")
# Status: VALID
# Parsed:
#   intensity: #
#   epistemic: ⊕
#   completeness: ∃F
#   subject: Negation_Mapping
#   relations: [⊂]
#   objects: [Connective_Mapping]
```

---

## Scenario 2: Repository CI/CD Validation

Richard maintains a public GitHub repository of his framework session logs. He wants to ensure all labels stay compliant as the repository evolves.

### Step 1: Set up CI check

Richard adds a `.github/workflows/validate-labels.yml` workflow:

```yaml
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
      
      - name: Validate all labels
        run: |
          python3 << 'EOF'
          import re
          from pathlib import Path
          import sys
          sys.path.insert(0, 'tools')
          from validate_label import validate_label
          
          failed = []
          
          # Find all markdown files
          for file in Path('.').rglob('*.md'):
              if file.name in ['README.md', 'CHANGELOG.md']:
                  continue
              
              with open(file) as f:
                  content = f.read()
              
              # Extract labels (pattern: ~∃F: or !⊕∃f:, etc.)
              pattern = r'[!~#@%][∃⊨⊕∴](?:∃F\+|∃F|∃f|∄F|§|⊣)(?:∈\w+)?: [^\n]+'
              labels = re.findall(pattern, content)
              
              for label in labels:
                  result = validate_label(label)
                  if not result.valid:
                      failed.append((file, label, result.errors))
          
          if failed:
              print("Label validation failed:\n")
              for file, label, errors in failed:
                  print(f"  {file}: {label}")
                  for error in errors:
                      print(f"    ✗ {error}")
              sys.exit(1)
          
          print(f"✓ All labels validated successfully")
          EOF
```

### Step 2: Author submits PR

A contributor adds a new session log with labels:

```markdown
# Session: March 2026 - Extending Rule D

~∃F: Extended_Rule_D
~⊕∃F: Graph_Inference-v2.1.0 ⊢ Cumulative_Knowledge
#∃F: Session_Persistence ∘ Rule_D
```

### Step 3: CI validates before merge

The validator runs. It finds that the second label uses hyphens and dots (for version number), which the **updated BNF now supports**:

```
✓ ~∃F: Extended_Rule_D
✓ ~⊕∃F: Graph_Inference-v2.1.0 ⊢ Cumulative_Knowledge
✓ #∃F: Session_Persistence ∘ Rule_D
```

The PR passes CI. Without the BNF refinement, this label would have failed.

---

## Scenario 3: Cross-Session Label Linking

Richard wants to check if any new labels in this session connect to previous sessions via Rule D inference.

### Step 1: Load previous session labels

From his session log, Richard extracts all `∃F` labels from previous sessions:

```python
previous_labels = {
    "Strategic_Labelling_Framework": "~∃§: Strategic_Labelling_Framework",
    "Curry_Howard_Isomorphism": "~⊕∃F: Curry_Howard_Isomorphism",
    "Type_System": "@⊕∃F: Type_System",
    # ... more from earlier sessions
}
```

### Step 2: Validate new labels

The current session produces new labels:

```python
new_labels = [
    "~⊕∃F: Type_Signature_Generation ⊣",
    "~⊨∃F: Propositions_As_Types",
    "~⊕∴∃F: Curry_Howard ⊢ Code_Generation",  # Derived via Rule D
]

# Validate each
for label in new_labels:
    result = validate_label(label)
    assert result.valid, f"Label invalid: {result.errors}"
```

### Step 3: Build the inference graph

Claude manually identifies relational connections (this could be automated):

```python
connections = [
    ("Type_Signature_Generation", "⊢", "Code_Generation"),
    ("Curry_Howard", "⊢", "Code_Generation"),
    ("Propositions_As_Types", "⊂", "Type_System"),
]

# These would then feed into Rule D to derive:
# Curry_Howard ⊢ Code_Generation (from transitivity)
# Type_Signature_Generation ⊢ Propositions_As_Types (if connected)
```

The validator ensures all labels in this chain conform to the grammar, making the inference chain itself trustworthy.

---

## Scenario 4: Validator in an Audit Prompt

Claude is executing the canonical audit prompt. The prompt instructs:

> *"For each idea, produce one label. Use the validator to check each label before returning."*

Claude generates and validates in a loop:

```python
session_ideas = [
    "A system that learns from its own errors",
    "Proof obligations as code targets",
    "Accumulation of knowledge across time",
]

labels = []
for idea in session_ideas:
    # Generate label
    label = ai_generate_label(idea)
    
    # Validate
    result = validate_label(label)
    
    # If invalid, regenerate
    while not result.valid:
        print(f"⚠ Invalid label: {result.errors}")
        label = ai_generate_label(idea, feedback=result.errors)
        result = validate_label(label)
    
    labels.append(label)
    print(f"✓ {label}")
```

**Output:**
```
✓ #⊕∃F: Self_Error_Learning-v1.0
✓ ~⊕∃F: Proof_Obligations ⊣
~⊕∃F: Knowledge_Accumulation ∘ Rule_D
```

All labels returned are guaranteed valid.

---

## Scenario 5: Using the Refined BNF in Practice

A session produces ideas that need version tracking:

```
Original idea (v1.0):
~⊕∃F: Attention_Mechanism

Later refinement (v2.1):
~⊕∃F: Attention_Mechanism-v2.1 ⊢ Query_Key_Scaling-v1.0
```

The validator accepts both because the BNF now allows hyphens and dots:

```python
result1 = validate_label("~⊕∃F: Attention_Mechanism")
# VALID

result2 = validate_label("~⊕∃F: Attention_Mechanism-v2.1")
# VALID

result3 = validate_label("~⊕∃F: Attention_Mechanism-v2.1 ⊢ Query_Key_Scaling-v1.0")
# VALID
# Objects: [Query_Key_Scaling-v1.0]
```

Without the BNF refinement, result2 and result3 would fail with "Invalid subject name."

---

## Workflow Integration Summary

```
┌─────────────────────────────────────────────────────────────┐
│ User Session                                                │
├─────────────────────────────────────────────────────────────┤
│ Research → Logic Extraction → Utility → Code                │
│ (user generates ideas and labels)                           │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
    ┌────────────────────┐
    │ Audit Prompt       │
    │ (Claude: list all  │
    │  ideas with labels)│
    └────────┬───────────┘
             │
             ↓
    ┌────────────────────────────────────────┐
    │ Validator (NEW)                        │
    │ - Parse each label against schema      │
    │ - Emit hard errors & soft warnings     │
    │ - Return to user only if valid         │
    └────────┬─────────────────────────────────┘
             │
             ↓
    ┌──────────────────────────────────────┐
    │ Labelling Prompt                     │
    │ (Claude: produce final label set)    │
    │ (all labels pre-validated)           │
    └────────┬──────────────────────────────┘
             │
             ↓
    ┌──────────────────────────────────────┐
    │ Session Log (Persistent)             │
    │ - All labels validated               │
    │ - BNF conformant (refined)           │
    │ - Ready for Rule D inference         │
    └──────────────────────────────────────┘
             │
             ↓
    ┌──────────────────────────────────────┐
    │ CI/CD (optional)                     │
    │ - Repository-wide validation         │
    │ - Catch drift at merge time          │
    │ - Enforce consistency over time      │
    └──────────────────────────────────────┘
```

---

## Key Improvements Enabled

| Workflow Stage | Before | After |
| :---- | :---- | :---- |
| **Label generation** | Manual checking, easy to miss errors | Automated validation, format guaranteed |
| **Session archiving** | Labels might be informal or incomplete | All labels schema-compliant, machine-readable |
| **Cross-session linking** | Manual inspection, laborious | Rule D inference works on guaranteed-valid graphs |
| **Repository maintenance** | No enforcement mechanism | CI/CD validates every merge |
| **Version tracking** | Not officially supported | Full support via refined BNF |
| **AI integration** | AI systems guessing at format | AI validates own output before returning |

---

## Implementation Notes

The three refinements are **independent but synergistic**:

1. **Refinement 1 (BNF)** solves a formal correctness problem: the grammar was lying about what it permitted.
2. **Refinement 2 (Validator)** solves an enforcement problem: without tooling, the grammar remained aspirational.
3. **Refinement 3 (Integration guide)** solves a discoverability problem: the validator is only valuable if people know it exists and how to use it.

All three are needed together. The BNF refinement without the validator is still just documentation. The validator without clear integration points will be ignored. The integration guide without a working validator has no substance.

---

**See also:**
- `schema.md` — the refined formal grammar
- `tools/validate_label.py` — the implementation
- `tools/README.md` — usage and integration patterns
- `REFINEMENT_SUMMARY.md` — what changed and why
