# SLF Toolchain Specification v1.0

## 1. The Linker
Verifies that objects in relational links refer to existing subjects in the global Epistemic Environment (`Γ`) across files.

## 2. The Cognitive Linter
Flags "stale" proof obligations (`⊣`) or high-intensity blockers (`!∄F`) that have not transitioned stage within defined session intervals.

## 2.1. Staleness Thresholds (v2.8-alpha)
To prevent "Epistemic Rot," the Linter applies the following temporal weights:

- **Critical Pressure (`!∄F`)**: High-impact blockers must show a state transition within **1 session**. Failure to resolve or downgrade results in a `STAGNATION_ALERT`.
- **Standard Velocity (`⊣`)**: Proof obligations should transition to `∃F+` or be decomposed into `∃f` partials within **3 sessions**.
- **Heuristic Decay (`?`)**: Heuristic/speculative insights should be formalized with a confidence score `[n]` or promoted to `∃f` within **2 sessions**.

## 3. The Visualizer
Generates topological maps of the session graph, highlighting derived insights (`∴`) produced by Rule D and Rule E.

## 4. NLLE Automation
Natural Language Logic Extraction: identifies logical connectives in raw text to suggest preliminary `⊣` labels.
