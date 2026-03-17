%⊕∃F+: Audit_Prompt-v2.7Strategic Labelling Framework — Session Readiness Audit ProtocolGenerated via ⊕ — Richard, Claude, & Gemini, March 2026PurposeThis document provides the canonical prompt for auditing a session for Absolute Code-Readiness. It moves the framework from a tracking system to a reasoner by enforcing v2.7 generative semantics and conflict detection.The v2.7 Canonical Audit PromptCopy and paste the following prompt into an AI session along with the session history:Using the Strategic Labelling Framework v2.7, audit this session for code readiness.Step 1 — Label and Weight Ideas.For each distinct idea, produce a label following the v2.7 structure:[Intensity] [Epistemic] [Completeness] [Project∈] [Uncertainty] : [Subject] [Relation] [Object]Uncertainty Layer: Assign a confidence score [0.0-1.0] or a heuristic marker ? to each label.Naming: Use underscores for words and hyphens/dots for versioning (e.g., Module-v1.0.1).Step 2 — Generative Inference (Rules D & E).Scan the label graph for derived connections:Rule D (Transitivity): If $A \vdash B$ and $B \vdash C$, output the derived label: [Int] ∴ [Comp] : A ⊢ C.Rule E (Isomorphism): If $A \cong B$ and $B \vdash C$, output the derived label: [Int] ∴ [Comp] : A ⊢ C.Step 3 — Conflict Detection (Rule F).Check the environment ($\Gamma$) for Epistemic Dissonance:Identify any cases where $A \vdash B$ and $A \vdash \neg B$ coexist.If detected, halt the audit and flag the contradiction as a critical blocker.Step 4 — Identify Blockers and Code Targets.List all ∄F blockers with a description of what is missing.List all ⊣ proof obligations and provide the implied type signature.Step 5 — Assess Readiness.State the v2.7 readiness condition:∄F count: [n]∃f count: [n]⊣  count: [n]Conflict Status: [Clear / Dissonance Detected]Declaration:If ∄F = 0, ∃f = 0, ⊣ > 0, and Conflict Status = Clear, declare: SESSION IS CODE-READY.Step 6 — Prompt for Resolution.For each blocker or heuristic label (?), ask one precise question to move it toward ∃F+.Expected Output StructurePlaintext## v2.7 Session Labels
~⊕∃F[0.9]: Concept_A ⊢ Concept_B
#⊕∴∃F: Concept_A ⊢ Concept_C  <-- [Derived via Rule D/E]
~⊕∃F: Typed_Logic ⊣

## Generative Insights (∴)
∴ Concept_A ⊢ Concept_C 
  (Logic: Transitive morphism detected)

## Conflict Report (Rule F)
Status: Clear. No Epistemic Dissonance detected.

## Readiness Assessment
∄F: 0 | ∃f: 0 | ⊣: 1
Status: SESSION IS CODE-READY.
Reference: v2.7 Readiness ConditionA session transitions to implementation only when:Structural Completeness: Zero blockers (∄F) and zero partials (∃f).Logical Inhabitation: At least one typed proof obligation (⊣).Internal Consistency: Zero detected conflicts via Rule F.
