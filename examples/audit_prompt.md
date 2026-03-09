# audit_prompt.md
## Strategic Labelling Framework — Session Readiness Audit Prompt

*%⊕∃F+: Audit_Prompt · AI_Reference*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Purpose

This document provides the canonical prompt for auditing a session using the Strategic Labelling Framework. It is designed to be given to an AI system along with a session history. The AI will assess the session for code readiness, identify blockers, and prompt the user to resolve incomplete propositions before any implementation begins.

---

## When to Use This Prompt

Use this prompt when:

- A session has produced a number of ideas and you want to know if they are ready to become code
- You suspect there are gaps in the logic but cannot identify them precisely
- You want a formal record of what is complete, what is partial, and what is blocked
- You are handing a session off to a different AI tool or a collaborator

---

## The Canonical Audit Prompt

Copy and paste the following prompt to an AI system, preceded by the full session history:

---

> Using the Strategic Labelling Framework (schema below), audit this session for code readiness.
>
> **Step 1 — Label all ideas.**
> For each distinct idea, concept, or artefact in the session, produce a label following the canonical structure:
> `[Intensity] [Epistemic] [Completeness] [Project∈] : [Subject] [Relation] [Object]`
>
> Use these markers:
> - Intensity: `!` `~` `#` `@` `%` (exactly one, required)
> - Epistemic: `∃` `⊨` `⊕` (exactly one, required)
> - Completeness: `∃F` `∃f` `∃F+` `∄F` `§` `⊣` (exactly one, required)
> - Relations (optional, maximum three): `∈` `⊂` `⊢` `≅` `∘` `∧` `·` `↳` `⊣`
> - Multi-word names use underscore: `My_Concept`
>
> **Step 2 — Identify blockers.**
> List all `∄F` items. For each, provide a plain-language description of what is missing. These are blockers — they must be resolved before coding begins.
>
> **Step 3 — Identify partial ideas.**
> List all `∃f` items. For each, state whether it can be graduated to `∃F` with clarification, or whether it should be marked `∄F`.
>
> **Step 4 — Identify code targets.**
> List all `⊣` items. For each, provide the type signature that the label implies.
>
> **Step 5 — Assess readiness.**
> State the readiness condition explicitly:
> - `∄F` count: [n]
> - `∃f` count: [n]
> - `⊣` count: [n]
>
> If `∄F` = 0 and `∃f` = 0 and `⊣` > 0, declare: **SESSION IS CODE-READY.**
> If any blockers remain, declare: **SESSION IS NOT YET CODE-READY.** List what must be resolved.
>
> **Step 6 — Prompt for resolution.**
> For each `∄F` blocker, ask the user one precise question that would resolve it. Frame each question as: *"What is [the missing element]?"*
>
> Do not proceed to implementation until all blockers are resolved and the readiness condition is met.

---

## Expected Output Structure

An AI responding to this prompt should return output in the following structure:

```
## Session Labels

~⊕∃F: Concept_One ⊢ Concept_Two
#⊕∃f: Partial_Concept
∄F: Blocked_Concept — [description of what is missing]
~⊕∃F: Typed_Concept ⊣

## Blockers

∄F: Blocked_Concept
→ Missing: [plain-language description]
→ Question: What is [missing element]?

## Partial Ideas

∃f: Partial_Concept
→ Can graduate to ∃F if: [clarification needed]

## Code Targets

⊣: Typed_Concept
→ Type signature: typedConcept :: A -> B

## Readiness Assessment

∄F count: 1
∃f count: 1
⊣  count: 1

Status: NOT YET CODE-READY

Resolve before proceeding:
1. [Blocker description and resolution question]
2. [Partial idea — clarification needed]
```

---

## After Resolution

Once the user has resolved all blockers, re-run the audit prompt against the updated session. When the readiness condition is met, proceed to the labelling prompt (`labelling_prompt.md`) to produce a final session label set before implementation begins.

---

## Soft Warning Conditions

The auditing AI should flag the following with a soft warning rather than an error:

| Condition | Warning |
| :---- | :---- |
| Relation present, object absent | `⚠ Relation has no object — consider completing` |
| Subject name contains spaces | `⚠ Use underscore for multi-word names` |
| More than three relational symbols | `⚠ Maximum three relations per label exceeded` |
| `∄F` present with no description | `⚠ Blocker label should include a description of what is missing` |

Soft warnings do not block the audit. They are noted and returned to the user for review.

---

## Reference: Readiness Condition

```
∄F count = 0
∃f count = 0
⊣  count > 0
→  SESSION IS CODE-READY
```

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: labelling_prompt.md, session_example.md, schema.md*

