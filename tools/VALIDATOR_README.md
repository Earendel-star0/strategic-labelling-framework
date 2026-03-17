# tools/

Reference tools for the Strategic Labelling Framework.

## validate_label.py

A lightweight reference validator for Strategic Labelling Framework labels.

**Purpose:** Validate that labels conform to the canonical grammar defined in `schema.md`. Useful for:
- Catching format drift early
- AI-assisted label generation (check output before returning to user)
- CI/CD pipelines (validate all labels in a repository)
- Audit prompts (check session labels before declaring readiness)

### Installation

No external dependencies. Requires Python 3.7+.

```bash
python3 validate_label.py "~∃F: My_Concept"
```

### Usage

#### Command line

Validate a single label:
```bash
python3 validate_label.py "~∃F: Strategic_Labelling_Framework"
```

Output JSON:
```bash
python3 validate_label.py "~∃F: Concept ⊢ Other_Concept" --json
```

#### In Python

```python
from validate_label import validate_label

result = validate_label("~∃F: My_Concept ⊢ Related_Concept")

if result.valid:
    print(f"✓ Valid label")
    print(f"  Intensity: {result.parsed['intensity']}")
    print(f"  Epistemic: {result.parsed['epistemic']}")
    print(f"  Completeness: {result.parsed['completeness']}")
    print(f"  Subject: {result.parsed['subject']}")
    print(f"  Relations: {result.parsed['relations']}")
    print(f"  Objects: {result.parsed['objects']}")
else:
    for error in result.errors:
        print(f"✗ {error}")

for warning in result.warnings:
    print(f"⚠ {warning}")
```

### Validation Rules

The validator checks:

**Hard errors** (label is invalid):
- Missing or invalid intensity marker
- Missing completeness marker
- Invalid subject name (contains spaces, special characters)
- Unexpected characters in the prefix (intensity + epistemic + completeness layers)
- Missing colon separator or incorrect whitespace around it

**Soft warnings** (label is valid but flagged):
- Relation present but no object — e.g., `~∃F: Concept ⊢` (recommended: add object)
- Subject contains spaces — e.g., `~∃F: My Concept` (recommended: use underscore)
- More than three relational symbols — e.g., `~∃F: A ⊢ B ∧ C ∘ D ⊂ E`
- `∄F` label without description of what is missing

### Output

#### Text (default)

```
Label: ~∃F: Strategic_Labelling_Framework
Status: VALID
Parsed: [~] [∃] [∃F] : Strategic_Labelling_Framework
```

#### JSON

```json
{
  "label": "~∃F: Strategic_Labelling_Framework",
  "valid": true,
  "errors": [],
  "warnings": [],
  "parsed": {
    "intensity": "~",
    "epistemic": "∃",
    "completeness": "∃F",
    "project": null,
    "subject": "Strategic_Labelling_Framework",
    "relations": [],
    "objects": []
  }
}
```

### Integration Points

#### AI-assisted label generation

When prompting an AI to generate labels (e.g., in an audit or labelling prompt), the AI should validate its own output before returning:

```python
# Pseudo-code for an AI system
user_request = "Label these ideas from my session..."

# Generate labels
labels = ai_generate_labels(user_request)

# Validate each
for label in labels:
    result = validate_label(label)
    if not result.valid:
        # Regenerate or return error
        flag_for_user_review(label, result.errors)

# Return only valid labels
return [label for label in labels if validate_label(label).valid]
```

#### Repository CI/CD

Validate all labels in a repository before merge:

```bash
#!/bin/bash
# ci-check-labels.sh

echo "Validating all labels in repository..."

# Find all files and extract labels (pattern: [marker]label format)
# Then validate each

failed=0
for file in $(find . -name "*.md" -type f); do
    # Extract labels (simplified grep; a real implementation would parse more carefully)
    grep -o '~[⊨∃⊕∴]∃F[^:]*:' "$file" | while read label; do
        if ! python3 tools/validate_label.py "$label" > /dev/null 2>&1; then
            echo "✗ Invalid: $label in $file"
            failed=1
        fi
    done
done

exit $failed
```

#### Audit prompts

When using the canonical audit prompt, the AI can validate labels as it generates them:

```
[Audit prompt: list all ideas and their labels]

For each label the AI generates, it validates:
- Intensity: !, ~, #, @, % (exactly one)
- Epistemic: ∃, ⊨, ⊕, ∴ (exactly one)
- Completeness: ∃F, ∃f, ∃F+, ∄F, §, ⊣ (exactly one)
- Subject: alphanumeric, underscores/hyphens allowed, no spaces
- Relations: maximum three per label

Then returns the label set only if all labels are valid.
```

### Test fixtures

The validator includes fixture labels from the framework's documented examples:

```python
FIXTURES = [
    "~∃§: Strategic_Labelling_Framework",
    "!⊕∃F: EGAP-v2.0.1 ⊢ Garden's_Tensor_Logic",
    "#∃F: Adaptive_Waypoint_System-v1.1",
    "@⊕∃f: Category_Theory ⊂ Protocols",
    "%⊨∃F: App_Scripts · Permission_Reset",
    "~∃F: Σ(Protocol_Design, Med_Viz) ⊢ Epistemic_Node ∧ Structural_Integrity",
    "~⊕∃f: Curry_Howard ⊣",
    "~∴∃F: Category_Theory ⊢ Intersubjective_Communication",
]

# All should validate without error
for label in FIXTURES:
    assert validate_label(label).valid
```

### Future enhancements

Potential additions to the validator:
- **Relation type checking** — validate that relational morphisms make semantic sense (e.g., prevent nonsensical chains)
- **Session graph validation** — check that ⊢ relations form a DAG (no cycles)
- **Cross-file label resolution** — in a multi-file repository, check that objects in relations refer to existing subjects
- **Linter mode** — return detailed suggestions for improving label clarity (e.g., "this looks like a blocker, consider marking ∄F")

---

**See also:**
- `schema.md` — formal grammar and canonical rules
- `examples/audit_prompt.md` — how to use the validator in audits
- `PHILOSOPHY.md` — why epistemic honesty matters
