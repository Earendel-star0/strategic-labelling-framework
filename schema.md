schema.md
Strategic Labelling Framework — Formal Grammar
#∃F+: Canonical syntax reference
Generated via ⊕ — Richard & Claude, March 2026

Purpose
This document defines the formal grammar of the Strategic Labelling Framework. It exists so that labels can be written consistently by humans, parsed reliably by AI systems, and extended without ambiguity as the framework grows.
A label that follows this grammar is valid. A label that does not is flagged with a soft warning — it is not rejected, but it is marked for review.

The Canonical Structure
[Intensity] [Epistemic] [Completeness] [Project∈] : [Subject] [Relation] [Object]
Whitespace is significant only around the colon separator. The colon must have exactly one space on each side.
VALID:   ~∃F: Strategic_Labelling_Framework
INVALID: ~∃F:Strategic_Labelling_Framework
INVALID: ~∃F : Strategic_Labelling_Framework

Field Definitions
1. Intensity [Intensity]
Required. Exactly one. No exceptions.
SymbolMeaning!Powerful / high impact~Insight / idea#Systemic / mechanical@Learning / accumulated knowledge%Document / record of process
VALID:   !∃F: EGAP_v2
INVALID: !~∃F: EGAP_v2        ← two intensity markers
INVALID: ∃F: EGAP_v2          ← missing intensity marker

2. Epistemic Origin [Epistemic]
Required. Exactly one. No exceptions.
SymbolMeaning∃Self-generated⊨Received / taught⊕Co-instantiated with AI∴Derived by the framework (Rule D)
VALID:   ~∃F: Concept
VALID:   ~⊨F: Concept
VALID:   ~⊕F: Concept
VALID:   ~∴F: Concept
INVALID: ~∃⊕F: Concept       ← two epistemic markers
INVALID: ~F: Concept          ← missing epistemic marker
Note on ∴: The derived marker appears automatically when Rule D (Structural Composition) infers a transitive relation in the session graph. Users do not typically create ∴ labels manually — they are produced by framework inference. See operational_semantics.md for details.

3. Completeness [Completeness]
Required. Exactly one.
SymbolMeaning∃FWell-formed / relatively complete∃fPartial / emerging∃F+Fully complete / stable∄FIncomplete / something missing§Root / foundational document⊣Typed but unimplemented (Curry-Howard extension)
Note: When § is used as the completeness marker, it implies foundational status and does not combine with ∃F, ∃f, or ∃F+.
VALID:   ~∃F: Concept
VALID:   ~∃§: Strategic_Labelling_Framework
INVALID: ~∃F§: Concept        ← two completeness markers

4. Project Membership [Project∈]
Optional.
Used to situate a label within a named project or domain. Written as ∈ProjectName immediately after the completeness marker, before the colon.
VALID:   #∃F∈MHD: Ethical_App_Building
VALID:   #∃F: Ethical_App_Building       ← project membership omitted

5. Subject [Subject]
Required.
The name of the idea, artefact, or concept being labelled. Multi-word names use underscore convention; versioning and domain qualifiers use hyphen.
VALID:   ~∃F: Strategic_Labelling_Framework
VALID:   ~∃F: EGAP-v2.0.1
VALID:   ~∃F: Category-Theory
INVALID: ~∃F: Strategic Labelling Framework   ← spaces in subject name
Naming philosophy: Subject names are identifiers. They appear in session logs and in relational links across sessions. Underscores join words into a single identifier (Strategic_Labelling_Framework). Hyphens separate version numbers or domain qualifiers from the core name (EGAP-v2.0.1, Permission-Reset-Script). This convention keeps identifiers machine-readable and human-parseable across the framework's lifetime.

6. Relation [Relation]
Optional. Maximum three relational symbols per label.
Relations connect the Subject to an Object. They are drawn from the relational layer of the framework.
SymbolMeaning∈Belongs to / is an element of⊂Is a subset of / contained by⊢Yields / proves / demonstrates≅Isomorphic / structurally identical∘Composition / transforms into∧Logical AND / also·Lightweight sub-element separator↳Nested under / drilling into⊣Typed but unimplemented (as relational: needs proof)
Relations may be chained up to a maximum of three:
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic ∧ Structural_Integrity
VALID:   !⊕∃F: EGAP ⊢ Tensor_Logic ∧ Structural_Integrity ∘ Garden
INVALID: !⊕∃F: EGAP ⊢ A ∧ B ∘ C ⊂ D    ← four relations, exceeds maximum

7. Object [Object]
Optional but recommended.
The thing the Subject relates to. Follows the same naming convention as Subject — underscore for multi-word names, hyphen for versioning.
When a relation is present but no object is given, the label is valid but flagged with a soft warning:
VALID (flagged):   ~∃F: Concept ⊢        ← relation present, object missing
VALID:             ~∃F: Concept ⊢ Other_Concept

Soft Warnings
A soft warning does not invalidate a label. It flags it for review. The following conditions trigger a soft warning:
ConditionWarningRelation present, object absent⚠ Relation has no object — consider completingSubject name contains spaces⚠ Use underscore for multi-word namesMore than three relational symbols⚠ Maximum three relations per label exceededCompleteness marker missing⚠ Completeness stage not specified∄F present with no description⚠ Blocker label should include a description of what is missing
A soft warning in an audit context signals a potential ∄F — something that may need resolution before the idea can be typed or implemented.

Complete Grammar in BNF Notation
For those building parsers or AI prompts around this schema:
label         ::= intensity epistemic completeness [project] ":" SPACE subject [relations]
intensity     ::= "!" | "~" | "#" | "@" | "%"
epistemic     ::= "∃" | "⊨" | "⊕" | "∴"
completeness  ::= "∃F+" | "∃F" | "∃f" | "∄F" | "§" | "⊣"
project       ::= "∈" name
subject       ::= name
relations     ::= SPACE relation [SPACE relation [SPACE relation]]
relation      ::= relop [SPACE object]
relop         ::= "∈" | "⊂" | "⊢" | "≅" | "∘" | "∧" | "·" | "↳" | "⊣"
object        ::= name
name          ::= word ("_" word)* | word ("-" word)*
word          ::= [A-Za-z0-9]+
SPACE         ::= " "
Key changes from previous grammar:

name now permits underscore (for multi-word identifiers) and hyphen (for versioning/qualification)
word remains alphanumeric — special characters are not permitted within words themselves, only as separators between words
∴ (derived marker) added to epistemic options — typically produced by Rule D inference, not user-created
This broadened grammar now matches actual practice in all documented examples

Note: ∃F+ must be matched before ∃F to avoid partial matching.

Valid Label Examples
~∃§: Strategic_Labelling_Framework
!⊕∃F: EGAP-v2.0.1 ⊢ Garden's_Tensor_Logic
#∃F: Adaptive_Waypoint_System-v1.1
@⊕∃f: Category_Theory ⊂ Protocols
%⊨∃F: App_Scripts · Permission_Reset
~∃F: Σ(Protocol_Design, Med_Viz) ⊢ Epistemic_Node ∧ Structural_Integrity
~⊕∃f: Curry_Howard ⊣
~∴∃F: Category_Theory ⊢ Intersubjective_Communication

Invalid Label Examples
!~∃F: Concept                 ← two intensity markers
∃F: Concept                   ← missing intensity marker
~F: Concept                   ← missing epistemic marker
~∃F:Concept                   ← missing space after colon
~∃F: My Concept               ← spaces in subject name (use underscore)
~∃F: A ⊢ B ∧ C ∘ D ⊂ E       ← five relations, exceeds maximum of three

Versioning
This schema reflects Strategic Labelling Framework v2.5.
For a full history of changes, see CHANGELOG.md.

This document is part of the Strategic Labelling Framework repository.
See also: README.md, PHILOSOPHY.md, curry_howard_extension.md
