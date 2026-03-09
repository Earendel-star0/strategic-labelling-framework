# labelling_prompt.md
## Strategic Labelling Framework — Session Labelling Prompt

*%⊕∃F+: Labelling_Prompt · AI_Reference*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Purpose

This document provides the canonical prompt for labelling a session using the Strategic Labelling Framework. It is designed to be given to an AI system along with a session history. The AI will produce a complete, schema-compliant label set for every idea, artefact, and transition in the session.

This prompt is distinct from the audit prompt. The audit prompt assesses readiness. This prompt produces the persistent label set — the map of thinking that accumulates across sessions.

---

## When to Use This Prompt

Use this prompt when:

- A session has concluded and you want a permanent record of what was produced
- You want to feed session outputs into a knowledge graph or second-brain system
- A session has passed the readiness audit and you want a final label set before implementation
- You are beginning a new session and want to carry forward the label set from a previous one

---

## The Canonical Labelling Prompt

Copy and paste the following prompt to an AI system, preceded by the full session history:

---

> Using the Strategic Labelling Framework (schema below), produce a complete label set for this session.
>
> **Instructions:**
>
> For each distinct idea, concept, artefact, insight, or document produced in this session, generate one label following the canonical structure:
> `[Intensity] [Epistemic] [Completeness] [Project∈] : [Subject] [Relation] [Object]`
>
> **Grammar rules:**
> - Intensity: `!` `~` `#` `@` `%` — exactly one, always required
> - Epistemic: `∃` `⊨` `⊕` — exactly one, always required
> - Completeness: `∃F` `∃f` `∃F+` `∄F` `§` `⊣` — exactly one, always required
> - Relations: optional, maximum three per label, drawn from: `∈` `⊂` `⊢` `≅` `∘` `∧` `·` `↳` `⊣`
> - Objects: optional but recommended — if a relation is present, provide an object
> - Multi-word names: underscore convention — `My_Concept`
> - Whitespace: one space on each side of the colon separator only
>
> **For each label, provide:**
> 1. The label itself
> 2. A one-line justification of the intensity, epistemic origin, and completeness choice
> 3. Any relational connections to other labels in this session
>
> **Epistemic origin guidance:**
> - `∃` — the user brought this idea into the session independently
> - `⊨` — the idea was received from an external source (documentation, teaching, prior knowledge)
> - `⊕` — the idea emerged in the conversation between user and AI; neither party held it complete before the session
>
> **Completeness guidance:**
> - `∃f` — the idea is present but not fully structured; edges are undefined
> - `∃F` — the idea is coherent and has a logical structure
> - `∃F+` — the idea has been implemented, tested, or fully resolved
> - `∄F` — the idea has a gap; something is missing
> - `⊣` — the idea has a type signature but no implementation yet
> - `§` — the idea is foundational; other ideas depend on it
>
> **Output format:**
>
> Return the label set as a structured list. After the label set, return:
> - A summary of completeness distribution (`∃f`, `∃F`, `∃F+`, `∄F`, `⊣` counts)
> - A list of relational connections between labels (the session graph)
> - Any soft warnings triggered

---

## Expected Output Structure

```
## Session Label Set

~∃§: Strategic_Labelling_Framework
→ Justification: foundational insight, self-generated, root document
→ Relations: none (root)

#⊕∃F: Four_Stage_Pipeline ⊢ Code_Generation
→ Justification: systemic, co-instantiated, well-formed
→ Relations: Four_Stage_Pipeline ⊢ Code_Generation

~⊕∃F: Session_Readiness_Condition ⊢ Audit_Prompt
→ Justification: insight, co-instantiated, well-formed
→ Relations: Session_Readiness_Condition ⊢ Audit_Prompt

#⊕∃F: borrowBook ⊣
→ Justification: systemic, co-instantiated, typed but unimplemented
→ Relations: borrowBook ⊣ (proof obligation)

## Completeness Distribution

∃f:   0
∃F:   3
∃F+:  1
∄F:   0
⊣:    1
§:    1

## Session Graph

~∃§: Strategic_Labelling_Framework
  ↳ #⊕∃F: Four_Stage_Pipeline ⊢ Code_Generation
  ↳ ~⊕∃F: Session_Readiness_Condition ⊢ Audit_Prompt
  ↳ #⊕∃F: borrowBook ⊣

## Soft Warnings

None.
```

---

## Carrying Labels Forward

The label set produced by this prompt is the persistent output of the session. To carry it into a new session:

1. Save the label set to your knowledge system
2. At the start of the next session, present the label set to the AI with the following instruction:

> *"These are the active labels from my previous session. Please treat ⊣ items as open proof obligations, ∄F items as unresolved blockers, and ∃F items as available propositions for this session."*

This ensures continuity across sessions. `∃f` items carry forward as open questions. `∃F+` items are closed. `⊣` items remain as code targets until implemented.

---

## Relationship to the Audit Prompt

| Audit Prompt | Labelling Prompt |
| :---- | :---- |
| Assesses readiness | Produces the label set |
| Identifies blockers | Records all ideas |
| Prompts for resolution | Maps the session graph |
| Run during the session | Run at the end of the session |
| Output: readiness decision | Output: persistent label set |

Use the audit prompt to determine if a session is ready to produce code. Use the labelling prompt to record what the session produced.

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: audit_prompt.md, session_example.md, schema.md*
