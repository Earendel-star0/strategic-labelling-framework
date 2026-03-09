# session_example.md
## Strategic Labelling Framework — Annotated Session Example

*%⊕∃F: Session_Example · AI_Reference*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Purpose

This document demonstrates the Strategic Labelling Framework applied to a real session. It is written for AI systems using the framework as a reference pattern. Every label is shown with its justification. Every transition between completeness stages is made explicit.

The source session covers: Curry-Howard isomorphism → natural language logic extraction → the Strategic Labelling Framework → GitHub repository construction.

---

## Session Metadata

```
Session origin:     ⊕ (co-instantiated — Richard & Claude)
Session date:       March 2026
Readiness outcome:  Code-ready (∄F = 0, ∃f = 0, ⊣ > 0)
Documents produced: 6
```

---

## Stage 1 — Research Intake

Ideas arrive. Epistemic origin is marked. Completeness is assessed honestly.

---

**Label:** `@⊨∃f: Curry_Howard_Isomorphism`

- Intensity `@` — accumulated knowledge, foundational learning
- Epistemic `⊨` — received from external source (prior knowledge)
- Completeness `∃f` — partially understood, not yet structured for application
- No relations yet — idea is present but not connected

---

**Label:** `@⊕∃f: Propositions_As_Types`

- Intensity `@` — learning
- Epistemic `⊕` — emerged in conversation with AI
- Completeness `∃f` — the correspondence is named but not yet operationalised
- No relations yet

---

**Label:** `~⊕∃f: Natural_Language_Logic_Extraction`

- Intensity `~` — insight
- Epistemic `⊕` — co-instantiated
- Completeness `∃f` — the idea that connectives in natural language map to types is present but not formalised
- No relations yet

---

## Stage 2 — Logic Extraction

Logical skeletons are identified. `∃f` items that have clear structure graduate to `∃F`. Items with gaps are marked `∄F`.

---

**Label:** `#⊕∃F: Connective_Mapping ⊂ Logic_Extraction`

- Intensity `#` — systemic
- Epistemic `⊕` — co-instantiated
- Completeness `∃F` — the mapping table (if/then → function, and → product, or → sum) is well-formed
- Relation `⊂` — this is a subset of the broader Logic_Extraction process
- Object present: `Logic_Extraction`

**Transition:** `∃f → ∃F` — the logical skeleton was extracted and found to be complete

---

**Label:** `~⊕∃F: Type_Signature_Generation ⊣`

- Intensity `~` — insight
- Epistemic `⊕` — co-instantiated
- Completeness `∃F` — the proposition is well-formed
- Relation `⊣` — typed but unimplemented; this is a code generation target
- **This label is a proof obligation**

**Example proposition resolved in this session:**

```
Natural language: "A library member who is both registered and has
                   a book available on loan can borrow it, otherwise
                   return an error."

Logical skeleton: Registered ∧ BookAvailable → Loan ∨ Error

Type signature:   borrowBook :: (Registered, BookAvailable) -> Either Loan Error

Label:            #⊕∃F: borrowBook ⊣
```

---

**Label:** `∄F: Void_Type_Clarification`

- Completeness `∄F` — blocker identified
- Description: the handling of negation (`¬A → Void`) was noted but not fully operationalised for natural language extraction
- **Soft warning triggered:** `∄F` label should include description of what is missing ✓ (provided above)
- **Resolution required before code stage**

---

## Stage 3 — Utility

Well-formed ideas are examined for structural relationships. Isomorphisms are identified. Compositions are mapped.

---

**Label:** `#⊕∃F: Strategic_Labelling_Framework ≅ Type_System`

- Intensity `#` — systemic
- Epistemic `⊕` — co-instantiated
- Completeness `∃F` — the isomorphism is well-formed and stable
- Relation `≅` — the framework and a type system are structurally identical
- Object present: `Type_System`

**Justification:** The framework's layers map directly onto type-theoretic constructs:
- Intensity markers → value constructors
- Epistemic origin → provenance typing
- Completeness stages → inhabitedness
- Relational layer → morphisms

---

**Label:** `#⊕∃F: Four_Stage_Pipeline ⊢ Code_Generation`

- Intensity `#` — systemic
- Epistemic `⊕` — co-instantiated
- Completeness `∃F` — the pipeline (Research → Logic_Extraction → Utility → Code) is well-formed
- Relation `⊢` — the pipeline yields code generation
- Object present: `Code_Generation`

---

**Label:** `~⊕∃F: Session_Readiness_Condition ⊢ Audit_Prompt`

- Intensity `~` — insight
- Epistemic `⊕` — co-instantiated
- Completeness `∃F` — the readiness condition is formally defined
- Relation `⊢` — the condition yields the audit prompt
- Object present: `Audit_Prompt`

**Readiness condition defined:**
```
∄F count = 0
∃f count = 0
⊣  count > 0
→  Session declared code-ready
```

---

## Stage 4 — Blocker Resolution

All `∄F` items must be resolved before proceeding to code.

---

**Blocker:** `∄F: Void_Type_Clarification`

**Resolution prompt used:**
> *"What are the natural language indicators of negation that map to the Void type?"*

**Resolution:**
- *"not"*, *"cannot"*, *"never"*, *"impossible"* → `A -> Never` / `A -> Void`
- Negation in specifications is often a precondition (proof obligation) rather than a type

**Transition:** `∄F → ∃F`

**Updated label:** `#⊕∃F: Negation_Mapping ⊂ Connective_Mapping`

---

## Stage 4 — Code Readiness Audit

```
∄F count:  0    ✓
∃f count:  0    ✓
⊣  count:  2    ✓

Status: CODE-READY
```

**Active ⊣ items:**

```
#⊕∃F: borrowBook ⊣
~⊕∃F: Type_Signature_Generation ⊣
```

---

## Stage 5 — Code

Each `⊣` item becomes an implementation target. Completion moves the item to `∃F+`.

---

**Label:** `#⊕∃F+: borrowBook`

```haskell
borrowBook :: (Registered, BookAvailable) -> Either Loan Error
borrowBook (registered, available) =
  case (registered, available) of
    (Registered, BookAvailable) -> Left  (Loan registered available)
    _                           -> Right (Error "Loan conditions not met")
```

- Transition: `⊣ → ∃F+`
- The type constrained the implementation — no incorrect return type is possible
- The proof term satisfies the proposition

---

## Session Output Labels — Summary

```
@⊨∃f: Curry_Howard_Isomorphism           ← intake, not yet graduated
@⊕∃F: Propositions_As_Types              ← graduated during session
~∃§:  Strategic_Labelling_Framework      ← root document produced
#⊕∃F: Connective_Mapping ⊂ Logic_Extraction
#⊕∃F: Four_Stage_Pipeline ⊢ Code_Generation
#⊕∃F: Strategic_Labelling_Framework ≅ Type_System
~⊕∃F: Session_Readiness_Condition ⊢ Audit_Prompt
#⊕∃F+: borrowBook                        ← implemented
%⊕∃F+: Repository_Documents ∈ GitHub     ← six documents produced
```

---

## What This Example Demonstrates

- `∃f` items that cannot be fully typed are marked `∄F` and resolved before coding
- `⊣` is the formal handoff between thinking and building
- Soft warnings are informative, not blocking — the `∄F` label above included a description as prompted
- All relations have objects — no soft warnings triggered in the final label set
- The session produces a coherent graph: ideas connect to each other via `⊢`, `≅`, and `⊂`
- `∃F+` marks completion — the label closes when the proof term exists

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: audit_prompt.md, labelling_prompt.md, schema.md*
