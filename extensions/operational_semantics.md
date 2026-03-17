# operational_semantics.md
## Strategic Labelling Framework — Operational Semantics

*#⊕∃F+: Operational_Semantics · Formal_Execution_Rules*
*Generated via ⊕ — Richard, Claude, & Gemini, March 2026*

---

## Purpose

While the schema defines the *grammar* of the Strategic Labelling Framework, the operational semantics define its *execution*. For the framework to act as an ontological compiler, it must possess formal rules dictating how an epistemic state transitions toward syntropy.

This document provides a Small-Step Operational Semantics model. It defines the legal morphisms between completeness states, ensuring that the transition from a partial thought (`∃f`) to a proof obligation (`⊣`) and finally to deployed code (`∃F+`) is mathematically rigorous.

---

## 1. The Epistemic Environment (State)

Execution occurs within the **Epistemic Environment**, denoted as `Γ`.

- `Γ` represents the set of all active, parsed labels within a given session.
- Execution is the iterative application of inference rules that transform `Γ` into a sequentially more structured state, `Γ'`.
- The system actively resists entropy by refusing to compile (evaluate to a final state) if contradictions or blocked propositions exist.

---

## 2. State Transition Rules (Execution Logic)

The compiler evaluates `Γ` by applying the following inference rules. Each rule states that if the preconditions above the line are met, the state transformation below the line is legally executed.

---

### Rule A — The Logic Extraction Rule (Formulation)

When a partial idea is formalised, the compiler extracts a logical proposition `P` and a type signature `τ`. The partial label is replaced, and the environment is updated with a well-formed proposition and an unimplemented proof obligation.

```
x^∃f ∈ Γ     extract(x) → (P, τ)
──────────────────────────────────────────────────
Γ → Γ ∖ {x^∃f} ∪ {x^∃F, P^⊣}
```

**In plain language:** A partial idea that can be given a logical skeleton and a type signature graduates to `∃F` and generates a `⊣` proof obligation.

---

### Rule B — The Blocker Resolution Rule (Unblocking)

When the environment encounters an uninhabited type or blocked concept (`∄F`), compilation halts. If the user provides the missing structural element `y`, the blocker is resolved into a well-formed proposition.

```
x^∄F ∈ Γ     resolve(x, y) → z^∃F
──────────────────────────────────────────────────
Γ → Γ ∖ {x^∄F} ∪ {z^∃F}
```

**In plain language:** A blocked idea cannot proceed. The user must supply what is missing. Once supplied, the blocker resolves to `∃F` and compilation may continue.

---

### Rule C — The Proof Realisation Rule (Implementation)

This is the moment of materialisation. If the environment holds a typed proof obligation `P^⊣`, and a program term `t` is provided that successfully satisfies the type `τ`, the obligation is discharged and the state transitions to complete (`∃F+`).

```
P^⊣ ∈ Γ     typecheck(t, τ) = true
──────────────────────────────────────────────────
Γ → Γ ∖ {P^⊣} ∪ {P^∃F+}
```

**In plain language:** A proof obligation is discharged when a correctly typed implementation is provided. The label transitions to `∃F+` — complete and stable.

---

### Rule D — The Structural Composition Rule (Graph Transitivity)

The relational layer executes automatically to increase the syntropy of the session graph. If proposition `A` yields `B`, and `B` yields `C`, the compiler infers the transitive morphism.

```
A ⊢ B ∈ Γ     B ⊢ C ∈ Γ
──────────────────────────────────────────────────
Γ → Γ ∪ {A ⊢ C}
```

**In plain language:** The session graph grows through inference. Transitive relationships are derived automatically — the compiler discovers connections the user did not explicitly state.

---

### Rule E — The Isomorphic Resolution Rule (Equivalence)

Derives morphisms across structurally identical propositions.

```
A ≅ B ∈ Γ     B ⊢ C ∈ Γ
──────────────────────────────────────────────────
Γ → Γ ∪ {A ∴ C}
```

### Rule F — The Conflict Detection Rule (Dissonance)

Halts compilation if contradictory propositions are derived.

```
A ⊢ B ∈ Γ     A ⊢ ¬B ∈ Γ
──────────────────────────────────────────────────
Γ → Halt(Epistemic_Dissonance)
```

## 3. Termination: The Code-Readiness Condition

A traditional compiler halts when it produces an executable binary or throws a fatal error. The Ontological Compiler halts when it reaches a state of **Absolute Code-Readiness**.

Execution terminates successfully if and only if the final epistemic environment `Γ_final` satisfies the following logical constraints:

```
Γ_final ⊨ (Σ∄F = 0) ∧ (Σ∃f = 0) ∧ (Σ⊣ > 0)
```

If `Γ` satisfies this condition, the semantic evaluation is complete. The system has successfully compiled human intent into a rigorous queue of verifiable proof obligations.

This condition is consistent with and extends the readiness condition defined in `audit_prompt.md`.

---

## 4. Relationship to the Schema

| schema.md | operational_semantics.md |
| :---- | :---- |
| Defines valid label structure | Defines valid label transitions |
| Grammar — what a label *is* | Execution — what a label *does* |
| Static | Dynamic |
| Checked at label creation | Evaluated across the session |

The schema and the operational semantics are complementary. A label can be grammatically valid (schema-compliant) but semantically blocked (Rule B applies). Both layers must be satisfied for a session to reach `Γ_final`.

---

## 5. The Epistemic Environment Across Sessions

`Γ` is not destroyed when a session ends. It is carried forward:

```
Γ_session_n → Γ_session_n+1
```

Labels marked `∃F+` are closed — they carry forward as stable propositions.
Labels marked `⊣` carry forward as open proof obligations.
Labels marked `∄F` carry forward as unresolved blockers.
Labels marked `∃f` carry forward as open questions.

This is the mechanism by which the framework accumulates knowledge across time rather than evaporating at session close.

---

## 6. Origin Note

The operational semantics were developed across three intelligences:

- The grammar and transformation model — Richard & Claude, March 2026
- The Small-Step Semantics formalisation and Rule D (Structural Composition) — Gemini, March 2026
- Integration and session persistence model — Richard, Claude & Gemini, March 2026

Rule D is a genuine extension to the framework. It makes the session graph **generative** — capable of deriving connections through inference rather than requiring explicit user input. This was not in the original design. It emerged through the collaborative audit process the framework itself prescribes.

`~⊕∃F+: Transitivity_Rule ∈ Operational_Semantics`

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: schema.md, curry_howard_extension.md, audit_prompt.md, CHANGELOG.md*
