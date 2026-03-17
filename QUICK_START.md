# Quick Start — Using the Refinements

Get started with the refined Strategic Labelling Framework in 5 minutes.

---

## What Changed?

Three things make the framework easier to use and maintain:

1. **Schema is now honest** — the BNF grammar now matches what the framework actually allows (hyphens, dots in names)
2. **Validator exists** — a tool that checks labels conform to the schema
3. **Integration patterns documented** — clear instructions for using the validator in sessions and CI/CD

**You don't need to change anything you're already doing.** All existing labels remain valid. The refinements just make the framework stricter and more toolable.

---

## Quick Start: Validating a Label

### Option 1: Command line (fastest)

```bash
python3 tools/validate_label.py "~∃F: My_Concept"
```

**Output:**
```
Label: ~∃F: My_Concept
Status: VALID
Parsed: [~] [∃] [∃F] : My_Concept
```

### Option 2: In Python (for AI systems or automation)

```python
from tools.validate_label import validate_label

result = validate_label("~∃F: My_Concept ⊢ Related_Concept")

if result.valid:
    print("✓ Label is valid")
    print(f"  Subject: {result.parsed['subject']}")
    print(f"  Relations: {result.parsed['relations']}")
else:
    print("✗ Label is invalid")
    for error in result.errors:
        print(f"  {error}")
```

---

## Examples: Old vs New

### Hyphens in names (now supported)

```
EGAP-v2.0.1 ⊢ Tensor_Logic
```

Before: ✗ Would fail ("invalid subject name")
After: ✓ Valid (hyphens allowed for versioning)

### Dots in version numbers (now supported)

```
System-v1.2.3
```

Before: ✗ Would fail
After: ✓ Valid

### All existing labels still work

```
~∃F: Strategic_Labelling_Framework          ✓ (unchanged)
~⊕∃F: Type_Signature_Generation ⊣           ✓ (unchanged)
#⊕∃F: borrowBook ⊢ Loan ∨ Error             ✓ (unchanged)
```

---

## Using in Your Session

When you label ideas in a session, optionally validate them:

```python
# Your idea
my_label = "~⊕∃F: New_Insight ⊢ Existing_Framework"

# Quick validation
from tools.validate_label import validate_label
result = validate_label(my_label)

if result.valid:
    print(f"✓ Ready to file: {my_label}")
else:
    print(f"⚠ Fix this: {result.errors}")
```

---

## Common Patterns

### Versioned ideas

```
~⊕∃F: Algorithm-v1.0 ⊢ Improvement-v1.1
```

Validated as:
```
Subject: Algorithm-v1.0
Object: Improvement-v1.1
```

### Domain-qualified ideas

```
#∃F: Permission-Reset-Script ∈ App_Infrastructure
```

Validated as:
```
Subject: Permission-Reset-Script
Object: App_Infrastructure
```

### Ideas with dotted version numbers

```
!∃F: Framework-v2.0.1 ⊢ Deployment-v2.0.2
```

Validated as:
```
Subject: Framework-v2.0.1
Object: Deployment-v2.0.2
```

---

## What the Validator Checks

**Hard errors** (label rejected):
- ✗ Missing intensity marker: `∃F: Concept`
- ✗ Invalid subject: `~∃F: My Concept` (use underscore)
- ✗ Wrong separator: `~∃F:Concept` (needs space after colon)

**Soft warnings** (label accepted, but flagged):
- ⚠ Relation without object: `~∃F: Concept ⊢`
- ⚠ Subject with spaces: `~∃F: My Concept`
- ⚠ Too many relations: `~∃F: A ⊢ B ∧ C ∘ D ⊂ E`

---

## For AI Systems Generating Labels

If you're building a system that generates labels (like in an audit prompt), validate the output:

```python
def audit_session(session_ideas):
    labels = []
    
    for idea in session_ideas:
        # Generate label
        label = llm_generate_label(idea)
        
        # Validate
        result = validate_label(label)
        
        if not result.valid:
            # Regenerate until valid
            label = llm_generate_label(idea, feedback=result.errors)
            result = validate_label(label)
            assert result.valid
        
        labels.append(label)
    
    return labels
```

---

## For Repository Maintainers

Add a simple CI check to your GitHub Actions workflow:

```yaml
- name: Validate labels
  run: |
    for file in *.md; do
      grep -o '[!~#@%][∃⊨⊕∴]∃F[^:]*:' "$file" | while read label; do
        python3 tools/validate_label.py "$label" || exit 1
      done
    done
```

This ensures every commit has valid labels.

---

## Schema Reference (One-Page)

```
[Intensity] [Epistemic] [Completeness] : [Subject] [Relation] [Object]

Intensity:    !, ~, #, @, %
Epistemic:    ∃, ⊨, ⊕, ∴
Completeness: ∃F+, ∃F, ∃f, ∄F, §, ⊣
Subject:      alphanumeric + underscore/hyphen/dot
Relation:     ∈, ⊂, ⊢, ≅, ∘, ∧, ·, ↳, ⊣ (max 3)
Object:       alphanumeric + underscore/hyphen/dot

Examples:
✓ ~∃F: My_Concept
✓ !⊕∃F: Algorithm-v2.0.1 ⊢ Result
✓ #∃F: Process ⊂ System ∧ Other_Aspect
```

---

## Troubleshooting

**Q: I'm getting "Invalid subject name"**
A: Check for spaces. Use underscores: `My_Concept` not `My Concept`. Hyphens and dots are fine: `v2.0.1`.

**Q: "Missing space after colon"**
A: Format is `[Markers] : [Subject]`. Notice the space after the colon.

**Q: "Relation has no object" warning**
A: This is allowed but flagged. If you meant to complete it, add the object: `Concept ⊢ Related_Concept`.

**Q: My label is valid but I want suggestions**
A: The validator returns soft warnings for common improvements. Check those first.

---

## Next Steps

1. **Read** `schema.md` for the formal rules
2. **Try** `tools/validate_label.py` on your labels
3. **Integrate** the validator into your workflow (session, CI, or AI system)
4. **Refer to** `INTEGRATION_GUIDE.md` for detailed patterns

---

**Files you now have:**
- `schema.md` — updated formal grammar
- `tools/validate_label.py` — the validator (CLI + library)
- `tools/README.md` — usage and integration patterns
- `REFINEMENT_SUMMARY.md` — what changed and why
- `INTEGRATION_GUIDE.md` — detailed workflows
- `QUICK_START.md` — this file

All refinements are backward compatible. Existing labels remain valid.
