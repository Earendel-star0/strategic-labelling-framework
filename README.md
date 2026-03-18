# Strategic Labelling Framework (SLF)

A symbolic annotation system for tracking the epistemic origin, intensity, and completeness of ideas across research, learning, and development sessions.

Developed collaboratively by Richard Barnes and Claude (Anthropic), with operational semantics contributed by Gemini (Google). All AI contributions are recorded under the `⊕` epistemic marker — co-instantiated with AI.

---

## Quick Start

A label takes the form:

```
[Intensity] [Epistemic] [Completeness] [Project∈] [Uncertainty] : [Subject] [Relation] [Object]
```

Example:

```
!⊕∃F: SLF ⊢ Curry_Howard_Isomorphism
```

---

## Layer Reference

### Layer 1 — Intensity (required, exactly one)

| Symbol | Meaning |
|--------|---------|
| `!` | Powerful / high impact |
| `~` | Insight / idea |
| `#` | Systemic / mechanical |
| `@` | Learning / accumulated knowledge |
| `%` | Document / record of process |

### Layer 2 — Epistemic Origin (required, exactly one)

| Symbol | Meaning |
|--------|---------|
| `∃` | Self-generated |
| `⊨` | Received / taught |
| `⊕` | Co-instantiated with AI |
| `∴` | Derived by the framework (Rule D / Rule E) |

### Layer 3 — Completeness (required, exactly one)

| Symbol | Meaning |
|--------|---------|
| `∃F` | Well-formed |
| `∃f` | Partial / emerging |
| `∃F+` | Fully complete |
| `∄F` | Incomplete / blocker |
| `§` | Root / foundational |
| `⊣` | Typed but unimplemented (Curry-Howard extension) |

### Layer 4 — Project Membership (optional)

Written as `∈ProjectName` immediately after the completeness marker.

### Layer 5 — Uncertainty (optional, v2.7)

| Symbol | Meaning |
|--------|---------|
| `[n]` | Confidence score 0.0–1.0 |
| `?` | Heuristic / speculative |

### Layer 6 — Relations (optional, max 3)

| Symbol | Meaning |
|--------|---------|
| `∈` | Member of |
| `⊂` | Subset of |
| `⊢` | Proves / produces |
| `≅` | Isomorphic to |
| `∘` | Composed with |
| `∧` | And / conjunction |
| `·` | Applied to |
| `↳` | Derives from |
| `⊣` | Left adjoint to / needs proof |

---

## Ontological Continuum

```
∅ ∘ ∃ ∘ ∃f ∘ ∃F ∘ ∃F+ ∘ §
```

Ground state → crosses into existence → emerging → well-formed → complete → foundational

---

## Four-Stage Pipeline

```
Research    →    Logic Extraction    →    Utility    →    Code
⊨ / ⊕            ∃f → ∃F               ∃F ⊢ ∃F+       ⊣ → ∃F+
```

---

## Repository Structure

```
strategic-labelling-framework/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── PHILOSOPHY.md
├── schema.md
├── strategic_labelling_framework.md
├── requirements.txt
├── docs/
│   ├── conceptual_overview.md
│   ├── rule_d_implications.md
│   └── toolchain_specification.md
├── examples/
│   ├── audit_prompt.md
│   ├── labelling_prompt.md
│   └── session_example.md
├── extensions/
│   ├── curry_howard_extension.md
│   ├── operational_semantics.md
│   └── rule_d_primer.md
└── tools/
    ├── validate_label.py       ← label validator (CLI + library)
    ├── linker.py               ← cross-file referential integrity
    ├── visualizer.py           ← Graphviz DOT graph generator
    ├── nlle_suggestor.py       ← natural language logic extraction
    ├── cognitive_linter.py     ← epistemic velocity monitor
    ├── journal_manager.py      ← session log writer
    └── README.md               ← toolchain usage guide
```

---

## Documentation

- [Schema and grammar rules](schema.md)
- [Full framework reference](strategic_labelling_framework.md)
- [Philosophy](PHILOSOPHY.md)
- [Curry-Howard extension](extensions/curry_howard_extension.md)
- [Operational semantics](extensions/operational_semantics.md)
- [Rule D primer](extensions/rule_d_primer.md)
- [Rule D implications](docs/rule_d_implications.md)
- [Toolchain specification](docs/toolchain_specification.md)
- [Toolchain usage guide](tools/README.md)
- [Changelog](CHANGELOG.md)

---

## Toolchain

The SLF ships with five tools, all in `tools/`. They share a common dependency on `validate_label.py` as their parsing layer.

```bash
# Install dependencies
pip install -r requirements.txt

# Validate a label
python3 tools/validate_label.py "~⊕∃F: My_Concept ⊢ Related_Concept"

# Check referential integrity across the repository
python3 tools/linker.py .

# Generate a graph visualisation
python3 tools/visualizer.py .
dot -Tpng graph.dot -o graph.png

# Suggest labels from natural language
python3 tools/nlle_suggestor.py "Category theory yields intersubjective communication."

# Write a session to the journal
python3 tools/journal_manager.py

# Run the cognitive linter against the session journal
python3 tools/cognitive_linter.py
```

---

## Licence

[MIT](LICENSE) — Richard Barnes and Claude (Anthropic), 2026.
