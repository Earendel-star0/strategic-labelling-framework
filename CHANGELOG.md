# CHANGELOG.md
## Strategic Labelling Framework — Version History

*Authorship: Richard & Claude & Gemini*

## v2.7 — March 2026 (Ontological Compiler Specification)

**Files:** `schema.md`, `strategic_labelling_framework.md`, `extensions/operational_semantics.md`, `docs/toolchain_specification.md`

- **Layer 7 — Uncertainty**: Formally introduced heuristic weight markers—confidence scores `[n]` and speculative markers `?`—into the canonical label structure and BNF grammar.
- **Enhanced Naming Convention**: Broadened the `name` rule in `schema.md` to support dot notation (e.g., `v2.0.1`), enabling machine-readable version components.
- **Rule E — Isomorphic Resolution**: Added operational logic to derive morphisms across structurally identical propositions within the Epistemic Environment (`Γ`).
- **Rule F — Conflict Detection**: Implemented safety logic to halt compilation upon identifying contradictory derived propositions (Epistemic Dissonance).
- **Toolchain Specification**: Authored new foundational document defining requirements for the SLF Linker, Cognitive Linter, Visualizer, and NLLE Automation.
---

## v2.5 — March 2026

**Files:** `schema.md`, `extensions/operational_semantics.md`

- Added `∴` (therefore) as fourth epistemic marker: derived by the framework via Rule D
- Closed open proof obligation: `~⊕∃f: Derived_Epistemic_Marker ⊣` → `~⊕∃F+: Derived_Epistemic_Marker`
- Updated schema to v2.5

---

## v2.4 — March 2026

**Files:** `README.md`, `schema.md`

- Rewrote README with correct table formatting and structure
- Fixed schema version reference from v2.2 to v2.4
- Added `extensions/rule_d_primer.md` (new)
- Repository renamed from `gemini-manifold` to `strategic-labelling-framework`
- Derived epistemic marker identified as open proof obligation: `~⊕∃f: Derived_Epistemic_Marker ⊣`

---

## v2.3 — March 2026

**File:** `extensions/operational_semantics.md` *(new)*

- Added formal Small-Step Operational Semantics — the execution model that transitions the framework from a static grammar into an active state machine
- Defined the Epistemic Environment `Γ` as the formal session state
- Four inference rules specified:
  - Rule A: Logic Extraction — `∃f → ∃F + ⊣`
  - Rule B: Blocker Resolution — `∄F → ∃F`
  - Rule C: Proof Realisation — `⊣ → ∃F+`
  - Rule D: Structural Composition — transitivity of `⊢` (graph inference)
- Termination condition formally stated as: `Γ_final ⊨ (Σ∄F = 0) ∧ (Σ∃f = 0) ∧ (Σ⊣ > 0)`
- Session persistence model defined — `Γ` carries forward across sessions
- Rule D is a genuine extension contributed by Gemini — the session graph is now generative
- Authorship: Richard, Claude, & Gemini
- Label transition: `~⊕∃f: Operational_Semantics ⊣` → `~⊕∃F+: Operational_Semantics`

---

## v2.2 — March 2026

**File:** `curry_howard_extension.md`

- Replaced payment/authentication example with library borrowing example
- Rationale: library domain is domain-agnostic, requires no financial or technical prior knowledge, and maps more clearly onto the logical connectives (`Registered ∧ BookAvailable → Loan ∨ Error`)

---

## v2.1 — March 2026

**Files:** `curry_howard_extension.md`, `PHILOSOPHY.md`

- Added `⊣` as a formal Layer 6 marker: *typed but unimplemented / needs proof*
- Introduced the four-stage pipeline: Research → Logic Extraction → Utility → Code
- Defined session readiness condition: `∄F` = 0 and `∃f` = 0 and `⊣` > 0
- Defined the audit prompt for AI-assisted session self-assessment
- Documented blocker resolution process: each `∄F` item treated as a Curry-Howard problem
- Added full correspondence table: Logic / Framework / Code
- Added `PHILOSOPHY.md` as foundational document (`~∃§`)
- Updated `⊕` attribution from "Gemini" to "AI" for tool-agnostic use

---

## v2.0 — March 2026

**File:** `strategic_labelling_framework.md`

- Replaced all emoji intensity markers (Layer 1) with ASCII equivalents:

| Removed | Replaced with | Meaning |
| :---- | :---- | :---- |
| 🚀 | `!` | Powerful / high impact |
| 💡 | `~` | Insight / idea |
| ⚙ | `#` | Systemic / mechanical |
| 📚 | `@` | Learning / accumulated knowledge |
| 🧾 | `%` | Document / record of process |

- Rationale: emoji are tokenised unpredictably by AI systems, splitting into multiple tokens and disrupting pattern matching and parsing. ASCII symbols are single, stable tokens and make the framework reliably machine-readable.
- All annotated examples updated to reflect new intensity markers
- Canonical label structure updated accordingly

---

## v1.0 — February 2026

**File:** `strategic_labelling_framework.md`

- Initial framework created via `⊕` — Richard & Claude
- Five layers defined: Intensity (emoji), Epistemic Origin, Completeness, Relational, Subject Markers
- Canonical label structure established: `[Emoji] [Epistemic] [Completeness] [Project∈] : [Subject] [Relation] [Object]`
- Garden → EGAP ontological continuum defined: `∅ ∘ ∃ ∘ ∃f ∘ ∃F ∘ ∃F+ ∘ §`
- Annotated examples provided covering all marker combinations
- Note recorded: *Hand off to Gemini for categorical morphism inference*

---

*For rationale behind design decisions, see PHILOSOPHY.md*
*For the type-theoretic extension, see curry_howard_extension.md*
