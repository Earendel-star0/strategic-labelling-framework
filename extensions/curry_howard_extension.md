# curry_howard_extension.md
## The Curry-Howard Extension to the Strategic Labelling Framework

*#⊕∃F+: Type-theoretic extension · code pipeline*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Overview

The Curry-Howard isomorphism states that there is a direct correspondence between logic and computation:

| Logic | Type Theory | This Framework |
| :---- | :---- | :---- |
| Proposition | Type | `∃F` — a well-formed idea |
| Proof | Program | `∃F+` — a completed implementation |
| Unprovable | Uninhabited type | `∄F` — something missing |
| Unproven | Typed but unimplemented | `⊣` — the handoff point |

This extension formalises how the Strategic Labelling Framework maps onto that correspondence, and defines the pipeline from natural language research to working code.

---

## The `⊣` Marker

The central contribution of this extension is a single new marker:

**`⊣` — Typed but unimplemented. The proposition exists; the proof does not yet.**

This is the formal handoff point between thinking and building. An idea labelled `⊣` has:

- A well-defined logical structure (`∃F`)
- A type signature that can be written down
- No implementation yet

It is a **proof obligation** — a formal claim that something needs to be built, and that the specification is complete enough to build it.

Without `⊣`, the transition from idea to code is invisible. The user moves from thinking to building without a clear moment of readiness. `⊣` makes that moment explicit.

---

## Natural Language as the Source Layer

The pipeline begins not with code but with natural language. Spoken and written language contains logical structure that can be extracted and mapped directly to types.

### Connective Mapping

| Natural Language | Logical Connective | Type |
| :---- | :---- | :---- |
| *if...then*, *given...produce* | Implication A → B | Function type `A -> B` |
| *and*, *both...and* | Conjunction A ∧ B | Product type `(A, B)` |
| *or*, *either...or* | Disjunction A ∨ B | Sum type `Either A B` |
| *not*, *cannot*, *never* | Negation ¬A | `A -> Void` |
| *for any*, *for all* | Universal ∀x. P(x) | Generic function |
| *there exists*, *some* | Existential ∃x. P(x) | Interface / `impl Trait` |
| *optional*, *may* | A ∨ ⊤ | `Option<A>` / `Maybe A` |

### Extraction Process

Given a natural language specification, the extraction process is:

1. Identify logical connectives in the text
2. Name the propositions they connect
3. Write the type signature
4. Label the result `⊣`

**Example:**

> *"A library member who is both registered and has a book available on loan can borrow it, otherwise return an error."*

Logical skeleton: `Registered ∧ BookAvailable → Loan ∨ Error`

Type signature:
```haskell
borrowBook :: (Registered, BookAvailable) -> Either Loan Error
```

Label: `#⊕∃F: borrowBook ⊣`

The implementation is now **constrained** by the type. The types determine what is possible. The proof term — the program body — must satisfy the proposition.

---

## The Four-Stage Pipeline

The framework maps its four primary goals onto four logical stages:

```
Research → Logic Extraction → Utility → Code
⊨ / ⊕      ∃f → ∃F           ∃F ⊢ ∃F+   ⊣ → ∃F+
```

### Stage 1: Research (`⊨` / `⊕`)

Ideas arrive as `∃f` — partial, not yet structured. The epistemic origin is marked honestly: `⊨` for received knowledge, `⊕` for ideas that emerge in collaboration with AI.

Goal: accumulate raw propositions.

### Stage 2: Logic Extraction (`∃f → ∃F`)

Natural language is examined for its logical skeleton. Connectives are identified and mapped to types. Partial ideas that have clear logical structure graduate from `∃f` to `∃F`. Those that do not are marked `∄F` — something is missing.

Goal: produce well-formed propositions with type signatures.

### Stage 3: Utility (`∃F ⊢ ∃F+`)

Well-formed ideas are examined for structural relationships:

- `≅` — are two ideas isomorphic? Can one be derived from the other?
- `∘` — can ideas be composed into a pipeline?
- `Σ` — can related ideas be grouped into a reusable set?

Goal: produce abstract, reusable propositions that are domain-agnostic.

### Stage 4: Code (`⊣ → ∃F+`)

Every `⊣` item is a code generation target. The type signature already exists from Stage 2. The implementation is now constrained — the types determine what is possible. Completion moves the item to `∃F+`.

Goal: produce verified implementations where the type system enforces correctness.

---

## Session Readiness: Self-Audit

A session can assess its own readiness to produce code by auditing the completeness markers present:

| Marker | Meaning for Code Readiness |
| :---- | :---- |
| `∃F` | Proposition ready — can be typed |
| `⊣` | Typed — ready for implementation |
| `∃F+` | Complete — already implemented |
| `∄F` | **Blocker** — must resolve before coding |
| `∃f` | **Blocker** — too vague, needs logic extraction first |

**Readiness condition:** `∄F` count = 0 and `∃f` count = 0 and `⊣` count > 0.

When this condition is met, the session has formally declared itself ready to code.

### The Audit Prompt

To perform a session audit, present the session history to an AI with the following prompt:

> *"Using the Strategic Labelling Framework, audit this session for code readiness. List all ⊣ items that are ready for implementation. List all ∄F blockers with a plain-language description of what is missing. List all ∃f items that need logic extraction before they can be typed. Do not proceed to code until all blockers are resolved."*

The AI will return a structured list of readiness items and blockers. The user resolves each `∄F` blocker by completing the proposition. Each `∃f` item either graduates to `∃F` or is marked `∄F` if it cannot.

---

## Resolving Blockers

Each `∄F` blocker is itself a Curry-Howard problem:

> *What type would complete this proposition?*

The user is not being asked to write code. They are being asked to complete a logical statement. This is a lower cognitive load and a more precise task. An AI can guide this process reliably because the question is well-formed: *what is missing from this type?*

**Example blocker resolution:**

```
∄F: Authentication · failure case undefined

Resolution prompt: "What are the possible failure cases for authentication?"
User response: "Expired token, invalid credentials, account locked."

Resolved type:
data AuthError = TokenExpired | InvalidCredentials | AccountLocked

∄F → ∃F: Authentication · failure cases defined
⊣: authenticate :: Credentials -> Either AuthError Session
```

The blocker is resolved. The type is complete. The item is ready for implementation.

---

## Correspondence Table: Full Mapping

| Logic | Framework | Code |
| :---- | :---- | :---- |
| Proposition | `∃F` | Type signature |
| Proof | `∃F+` | Implementation |
| Implication | `A ⊢ B` | Function `A -> B` |
| Conjunction | `A ∧ B` | Struct / tuple `(A, B)` |
| Disjunction | `A \| B` | Enum / `Either A B` |
| Negation | `¬A` | `A -> Never` |
| Universal | `∀` | Generic / polymorphic |
| Existential | `∃` (relational) | Interface / trait |
| Uninhabited | `∄F` | Compile error / blocker |
| Unproven | `⊣` | Unimplemented function |
| Isomorphism | `≅` | Structural equivalence |
| Composition | `∘` | Function composition |

---

## Why This Matters

Most development failures are not implementation failures. They are specification failures. The logic had gaps that only surfaced as bugs — after the code was written, after the tests were run, after the system was deployed.

The Curry-Howard extension moves the point of failure detection upstream — to the logical level, before implementation begins. A `∄F` marker is a bug that was caught before it became code.

The type system enforces this. A well-typed program is a proved proposition. If the proposition was incomplete, the type system will not accept the proof. The framework makes that incompleteness visible to the user — and resolvable — before the compiler is ever invoked.

---

*This extension is part of the Strategic Labelling Framework repository.*
*See also: PHILOSOPHY.md, schema.md, examples/audit_prompt.md*
