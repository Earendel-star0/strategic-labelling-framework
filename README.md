# Strategic Labelling Framework (SLF)

A symbolic annotation system for tracking the epistemic origin, intensity, and completeness of ideas across research, learning, and development sessions.

Developed collaboratively by Richard Barnes and Claude (Anthropic), with operational semantics contributed by Gemini (Google). All AI contributions are recorded under the `⊕` epistemic marker — co-instantiated with AI.

---

## Quick Start

A label takes the form:
```
[Intensity] [Epistemic] [Completeness] [Relations] : Subject [Relation Object]
```

Example:
```
!⊕∃F ⊢ : SLF proves Curry_Howard_Isomorphism
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

### Layer 3 — Completeness (required, exactly one)

| Symbol | Meaning |
|--------|---------|
| `∃F` | Well-formed |
| `∃f` | Partial / emerging |
| `∃F+` | Fully complete |
| `∄F` | Incomplete / blocker |
| `§` | Root / foundational |
| `⊣` | Typed but unimplemented (Curry-Howard extension) |

### Layer 4 — Relations (optional, max 3)

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
| `⊣` | Left adjoint to |

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
├── docs/
│   ├── conceptual_overview.md
│   └── rule_d_implications.md
├── examples/
│   ├── audit_prompt.md
│   ├── labelling_prompt.md
│   ├── session_example.md
│   ├── evolution_example.py
│   ├── expressive_example.py
│   └── stability_example.py
└── extensions/
    ├── curry_howard_extension.md
    ├── operational_semantics.md
    └── rule_d_primer.md
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
- [Changelog](CHANGELOG.md)

---

## Licence

[MIT](LICENSE) — Richard Barnes and Claude (Anthropic), 2026.
