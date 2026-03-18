# schema.md
## Strategic Labelling Framework — Formal Grammar

*#∃F+: Canonical syntax reference*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Purpose

This document defines the formal grammar of the Strategic Labelling Framework. It exists so that labels can be written consistently by humans, parsed reliably by AI systems, and extended without ambiguity as the framework grows.

A label that follows this grammar is valid. A label that does not is flagged with a soft warning — it is not rejected, but it is marked for review.

---

## The Canonical Structure

```
[Intensity] [Epistemic] [Completeness] [Project∈] [Uncertainty] : [Subject] [Relation] [Object]
```

Whitespace is significant **only around the colon separator**. The colon must have exactly one space on each side.

```
VALID:   ~∃F: Strategic_Labelling_Framework
INVALID: ~∃F:Strategic_Labelling_Framework
INVALID: ~∃F : Strategic_Labelling_Framework
```

---

## Field Definitions

### 1. Intensity `[Intensity]`

**Required. Exactly one. No exceptions.**

| Symbol | Meaning |
| :---- | :---- |
| `!` | Powerful / high impact |
| `~` | Insight / idea |
| `#` | Systemic / mechanical |
| `@` | Learning / accumulated knowledge |
| `%` | Document / record of process |

```
VALID:   !∃F: EGAP-v2
INVALID: !~∃F: EGAP-v2       ← two intensity markers
INVALID: ∃F: EGAP-v2         ← missing intensity marker
```

---

### 2. Epistemic Origin `[Epistemic]`

**Required. Exactly one. No exceptions.**

| Symbol | Meaning |
| :---- | :---- |
| `∃` | Self-generated |
| `⊨` | Received / taught |
| `⊕` | Co-instantiated with AI |
| `∴` | Derived by the framework (Rule D / Rule E) |

```
VALID:   ~∃F: Concept
VALID:   ~⊨∃F: Concept
VALID:   ~⊕∃F: Concept
VALID:   ~∴∃F: Concept
INVALID: ~∃⊕∃F: Concept      ← two epistemic markers
INVALID: ~F: Concept          ← missing epistemic marker
```

**Note on `∴`:** The derived marker appears automatically when Rule D (Structural Composition) or Rule E (Isomorphic Resolution) infers a relation in the session graph. Users do not typically create `∴` labels manually — they are produced by framework inference. See `extensions/operational_semantics.md` for details.

---

### 3. Completeness `[Completeness]`

**Required. Exactly one.**

| Symbol | Meaning |
| :---- | :---- |
| `∃F` | Well-formed / relatively complete |
| `∃f` | Partial / emerging |
| `∃F+` | Fully complete / stable |
| `∄F` | Incomplete / something missing |
| `§` | Root / foundational document |
| `⊣` | Typed but unimplemented *(Curry-Howard extension)* |

Note: When `§` is used as the completeness marker, it implies foundational status and does not combine with `∃F`, `∃f`, or `∃F+`.

```
VALID:   ~∃F: Concept
VALID:   ~∃§: Strategic_Labelling_Framework
INVALID: ~∃F§: Concept        ← two completeness markers
```

---

### 4. Project Membership `[Project∈]`

**Optional.**

Used to situate a label within a named project or domain. Written as `∈ProjectName` immediately after the completeness marker, before the uncertainty marker and colon.

```
VALID:   #∃F∈MHD: Ethical_App_Building
VALID:   #∃F: Ethical_App_Building       ← project membership omitted
```

---

### 5. Uncertainty `[Uncertainty]`

**Optional. Layer 7 — introduced in v2.7.**

Assigns a confidence weight to a label. Two forms are permitted:

| Symbol | Meaning |
| :---- | :---- |
| `[n]` | Confidence score, where n is a float between 0.0 and 1.0 |
| `?` | Heuristic / speculative — confidence unquantified |

```
VALID:   ~⊕∃f[0.8]: Emergent_Pattern
VALID:   ~∃f?: Speculative_Morphism
INVALID: ~∃f[1.5]: Concept     ← score out of range
```

Heuristic labels (`?`) are monitored by the Cognitive Linter — they should be formalised with a score or promoted to `∃f` within the defined session threshold.

---

### 6. Subject `[Subject]`

**Required.**

The name of the idea, artefact, or concept being labelled. Multi-word names use underscore convention; versioning and domain qualifiers use hyphen; version components use dot notation.

```
VALID:   ~∃F: Strategic_Labelling_Framework
VALID:   ~∃F: EGAP-v2.0.1
VALID:   ~∃F: Adaptive_Waypoint_System-v1.1
INVALID: ~∃F: Strategic Labelling Framework   ← spaces in subject name
```

**Naming philosophy:** Subject names are identifiers. They appear in session logs and in relational links across sessions. Underscores join words into a single identifier (`Strategic_Labelling_Framework`). Hyphens separate version numbers or domain qualifiers from the core name (`EGAP-v2.0.1`). Dots separate version components (`v2.0.1`). This convention keeps identifiers machine-readable and human-parseable across the framework's lifetime.

---

### 7. Relation `[Relation]`

**Optional. Maximum three relational symbols per label.**

Relations connect the Subject to an Object. They are drawn from the relational layer of the framework.

| Symbol | Meaning |
| :---- | :---- |
| `∈` | Belongs to / is an element of |
| `⊂` | Is a subset of / contained by |
| `⊢` | Yields / proves / demonstrates |
| `≅` | Isomorphic / structurally identical |
| `∘` | Composition / transforms into |
| `∧` | Logical AND / also |
| `·` | Lightweight sub-element separator |
| `↳` | Nested under / drilling into |
| `⊣` | Typed but unimplemented *(as relational: needs proof)* |

Relations may be chained up to a maximum of three:

```
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic ∧ Structural_Integrity
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic ∧ Structural_Integrity ∘ Garden
INVALID: !⊕∃F: EGAP ⊢ A ∧ B ∘ C ⊂ D    ← four relations, exceeds maximum
```

---

### 8. Object `[Object]`

**Optional but recommended.**

The thing the Subject relates to. Follows the same naming convention as Subject.

When a relation is present but no object is given, the label is **valid but flagged** with a soft warning:

```
VALID (flagged):   ~∃F: Concept ⊢        ← relation present, object missing
VALID:             ~∃F: Concept ⊢ Other_Concept
```

---

## Soft Warnings

A soft warning does not invalidate a label. It flags it for review. The following conditions trigger a soft warning:

| Condition | Warning |
| :---- | :---- |
| Relation present, object absent | `⚠ Relation has no object — consider completing` |
| Subject name contains spaces | `⚠ Use underscore for multi-word names` |
| More than three relational symbols | `⚠ Maximum three relations per label exceeded` |
| Completeness marker missing | `⚠ Completeness stage not specified` |
| `∄F` present with no description | `⚠ Blocker label should include a description of what is missing` |

A soft warning in an audit context signals a potential `∄F` — something that may need resolution before the idea can be typed or implemented.

---

## Complete Grammar in BNF Notation

For those building parsers or AI prompts around this schema:

```
label         ::= intensity epistemic completeness [project] [uncertainty] ":" SPACE subject [relations]
intensity     ::= "!" | "~" | "#" | "@" | "%"
epistemic     ::= "∃" | "⊨" | "⊕" | "∴"
completeness  ::= "∃F+" | "∃F" | "∃f" | "∄F" | "§" | "⊣"
project       ::= "∈" name
uncertainty   ::= "[" float "]" | "?"
subject       ::= name
relations     ::= SPACE relation [SPACE relation [SPACE relation]]
relation      ::= relop [SPACE object]
relop         ::= "∈" | "⊂" | "⊢" | "≅" | "∘" | "∧" | "·" | "↳" | "⊣"
object        ::= name
name          ::= word (("_" | "-" | ".") word)*
word          ::= [A-Za-z0-9]+
float         ::= "0." [0-9]+ | "1.0"
SPACE         ::= " "
```

**Notes:**
- `∃F+` must be matched before `∃F` to avoid partial matching
- `name` permits underscore (multi-word), hyphen (versioning), and dot (version components) as separators — mixed separators are allowed within a single name (e.g. `EGAP-v2.0.1`)
- `∴` is typically produced by Rule D / Rule E inference, not written manually
- The BNF now supersedes the alternation form used in v2.6; the unified separator pattern correctly handles mixed separators such as `Algorithm-v2.0.1`

---

## Valid Label Examples

```
~∃§: Strategic_Labelling_Framework
!⊕∃F: EGAP-v2.0.1 ⊢ Tensor_Logic
#∃F: Adaptive_Waypoint_System-v1.1
@⊕∃f: Category_Theory ⊂ Protocols
%⊨∃F: App_Scripts · Permission_Reset
~∃F: Epistemic_Node ⊢ Structural_Integrity ∧ Session_Persistence
~⊕∃f: Curry_Howard ⊣
~∴∃F: Category_Theory ⊢ Intersubjective_Communication
~⊕∃f[0.7]: Neural_Manifold ≅ Geometric_Invariant
~∃f?: Speculative_Morphism
```

---

## Invalid Label Examples

```
!~∃F: Concept                 ← two intensity markers
∃F: Concept                   ← missing intensity marker
~F: Concept                   ← missing epistemic marker
~∃F:Concept                   ← missing space after colon
~∃F: My Concept               ← spaces in subject name (use underscore)
~∃F: A ⊢ B ∧ C ∘ D ⊂ E       ← five relations, exceeds maximum of three
```

---

## Versioning

This schema reflects **Strategic Labelling Framework v2.7**.
For a full history of changes, see `CHANGELOG.md`.

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: README.md, PHILOSOPHY.md, extensions/curry_howard_extension.md, extensions/operational_semantics.md*
