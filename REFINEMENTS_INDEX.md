# Refinements Package — File Index

This package contains three refinements to the Strategic Labelling Framework, completed in March 2026.

## Start Here

**→ `README.md`** — Executive summary of all refinements and what was delivered

**→ `QUICK_START.md`** — Get started using these refinements in 5 minutes

## Core Deliverables

### 1. Updated Schema
**`schema.md`** — Formal grammar with corrected BNF
- Permits hyphens and dots in identifiers (e.g., `EGAP-v2.0.1`)
- Deduped epistemic marker table
- Added naming philosophy section
- All examples updated
- **Use this** if you need to reference the formal grammar

### 2. Label Validator
**`tools/validate_label.py`** — Reference implementation
- Parses and validates labels
- CLI interface: `python3 validate_label.py "~∃F: Concept"`
- Python library: `from validate_label import validate_label`
- No external dependencies
- **Use this** to check individual labels or integrate into workflows

**`tools/README.md`** — Validator documentation
- Usage patterns (CLI, Python, CI/CD)
- Integration examples (sessions, audit prompts, repositories)
- Test fixtures
- Future enhancements
- **Use this** to understand how to integrate the validator

### 3. Integration & Documentation
**`REFINEMENT_SUMMARY.md`** — What changed and why
- Before/after comparison
- Rationale for each change
- Impact on framework
- **Use this** to understand the reasoning behind refinements

**`INTEGRATION_GUIDE.md`** — Real-world workflows
- 5 detailed scenarios showing validator in action
- Session workflows
- CI/CD setup
- Rule D inference integration
- **Use this** for concrete examples of refinements in practice

**`QUICK_START.md`** — Beginner's guide
- 5-minute overview
- Command-line examples
- Common patterns
- Troubleshooting
- **Use this** to get started quickly

## File Organization

```
refinements-package/
├── README.md                    ← Start here (executive summary)
├── QUICK_START.md              ← Get going in 5 minutes
├── REFINEMENT_SUMMARY.md       ← What changed and why
├── INTEGRATION_GUIDE.md        ← Detailed workflows
├── INDEX.md                    ← This file
├── schema.md                   ← Updated formal grammar
└── tools/
    ├── validate_label.py       ← The validator (production-ready)
    └── README.md               ← Validator usage guide
```

## How to Use This Package

### If you want to...

**...understand what changed**  
→ Read `README.md` (5 min), then `REFINEMENT_SUMMARY.md` (10 min)

**...start using the validator immediately**  
→ Read `QUICK_START.md` (5 min), then run validator on a label

**...integrate validator into a workflow**  
→ Read `INTEGRATION_GUIDE.md` and pick your scenario (10-20 min)

**...reference the formal grammar**  
→ Use `schema.md` (replaces old schema.md in main repo)

**...set up CI/CD validation**  
→ Follow pattern in `INTEGRATION_GUIDE.md` Scenario 2 or `tools/README.md`

**...use validator in AI-assisted sessions**  
→ Follow pattern in `INTEGRATION_GUIDE.md` Scenario 1

## Key Changes at a Glance

| What | Before | After | Why |
| :---- | :---- | :---- | :---- |
| **BNF** | Restricts names to underscores only | Allows hyphens and dots | Real labels use versions like `v2.0.1` |
| **Validation** | Manual/informal | Automated via tool | Framework rules should be enforceable |
| **Epistemic markers** | Duplicated `∴` in table | Single entry with note | Specification should have no redundancy |
| **Integration** | No documented patterns | Clear examples in guide | Framework should be easy to automate |

## For Different Roles

**Framework user (Richard):**
- Read: `QUICK_START.md`, then optional `INTEGRATION_GUIDE.md` Scenario 1
- Use: CLI validator when you want to check a label is valid

**AI system (Claude in sessions):**
- Understand: `tools/README.md` integration section
- Use: Import validator in audit/labelling prompts to validate own output

**Repository maintainer:**
- Read: `REFINEMENT_SUMMARY.md`, then `tools/README.md`
- Implement: CI/CD check from `INTEGRATION_GUIDE.md` or `tools/README.md`

**Developer integrating framework:**
- Study: `schema.md` (formal grammar)
- Reference: `tools/validate_label.py` (Python library)
- Learn: `tools/README.md` (API + integration patterns)

## Testing

All deliverables have been tested:
- ✓ Validator passes on 8 fixture labels
- ✓ Backward compatible (all existing labels validate)
- ✓ CLI and Python API both work
- ✓ JSON output serializes correctly

## Next Steps

1. **Choose your entry point** based on role above
2. **Read the relevant docs** (5-20 minutes)
3. **Try the validator** on one of your labels
4. **Integrate into your workflow** (optional but recommended)

## Questions?

Refer to:
- `QUICK_START.md` → Quick answers
- `tools/README.md` → Validator-specific questions
- `INTEGRATION_GUIDE.md` → Workflow questions
- `README.md` → Big picture questions

---

**Package created:** March 2026  
**Status:** Complete and ready for integration  
**Backward compatible:** Yes (all existing labels remain valid)
