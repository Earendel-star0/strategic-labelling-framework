# SLF Toolchain Specification v2.0

*#⊕∃F+: Toolchain_Specification · Framework_Infrastructure*
*Generated via ⊕ — Richard & Claude, March 2026*

---

## Overview

The SLF toolchain operationalises the framework. Where the schema defines what a label *is* and the operational semantics define what a label *does*, the toolchain enforces both — catching errors at the syntactic, referential, and temporal levels.

All tools are implemented in Python 3.7+ with no external dependencies except `pyyaml` (required by the Cognitive Linter and Journal Manager). All tools call `validate_label.py` as their shared parsing layer.

```
validate_label.py          ← shared parsing layer
       │
       ├── linker.py               (syntactic + referential)
       ├── visualizer.py           (syntactic + structural)
       ├── nlle_suggestor.py       (generative)
       ├── cognitive_linter.py     (temporal)  ← requires pyyaml
       └── journal_manager.py      (persistence) ← requires pyyaml
```

---

## 1. The Label Validator

**File:** `tools/validate_label.py`
**Status:** `∃F+`

Parses and validates individual labels against the canonical grammar defined in `schema.md`. The foundation of the toolchain — all other tools depend on it as a library.

**Checks performed:**
- Intensity marker present and valid (`!`, `~`, `#`, `@`, `%`)
- Epistemic marker present and valid (`∃`, `⊨`, `⊕`, `∴`)
- Completeness marker present and valid (`∃F+`, `∃F`, `∃f`, `∄F`, `§`, `⊣`)
- Optional project membership (`∈Name`)
- Optional uncertainty marker (`[0.0–1.0]` or `?`)
- Colon separator with correct whitespace
- Subject name matches `name` pattern (alphanumeric, `_`, `-`, `.`)
- Relations drawn from valid set, maximum three per label
- Objects present when relations are present (soft warning if absent)

**Output modes:** text (default), JSON (`--json`)
**Exit codes:** 0 = valid, 1 = invalid

---

## 2. The Linker

**File:** `tools/linker.py`
**Status:** `∃F+`

Verifies referential integrity across the repository. For every relational object in a label (`A ⊢ B` → object is `B`), the Linker checks that a corresponding subject exists somewhere in `Γ` across all scanned files.

**Algorithm:**
1. Walk all `.md` files in the target directory
2. For each line containing `:`, attempt validation
3. If valid: record subject → filename mapping; collect all objects
4. After full scan: for each object, check membership in subjects
5. Report any objects with no matching subject as broken links

**Known limitation:** name aliasing. `Curry_Howard` and `Curry_Howard_Isomorphism` are treated as distinct subjects even if they represent the same concept. Canonical naming discipline prevents most cases; fuzzy resolution is a future enhancement (`⊣`).

**Exit codes:** 0 = all links resolved, 1 = broken links detected

---

## 3. The Visualizer

**File:** `tools/visualizer.py`
**Status:** `∃F+`

Generates a Graphviz DOT file from the label graph. Nodes are subjects and objects; edges are relational links labelled with the relation symbol.

**Edge styling:**
- Derived relations (`∴` epistemic marker): dashed blue edges
- Explicit relations: solid black edges with relation label

**Output:** `graph.dot` (excluded from version control via `.gitignore`)

**Rendering:**
```bash
dot -Tpng graph.dot -o graph.png
dot -Tsvg graph.dot -o graph.svg
```

**Known open obligations (`⊣`):**
- Relation-type edge styling (distinct visual treatment for `⊢` vs `≅` vs `⊂`)
- Completeness-state node colouring (`∃F+` nodes distinct from `⊣` nodes)
- Example label filtering (exclude labels from documentation examples files)

---

## 4. The NLLE Suggestor

**File:** `tools/nlle_suggestor.py`
**Status:** `∃F+`

Automates Rule A (Logic Extraction) by identifying logical connectives in natural language input and suggesting preliminary labels. Implements the NLLE Automation component of the v2.7 toolchain specification.

**Connective mapping:**

| Pattern | Suggested relop |
| :---- | :---- |
| `if...then`, `yields`, `leads to`, `proves` | `⊢` |
| `same as`, `equivalent to`, `isomorphic` | `≅` |
| `part of`, `inside`, `contained in` | `⊂` |
| `and`, `also` | `∧` |
| `transforms into`, `becomes` | `∘` |

All suggested labels carry `∃f?` — partial and speculative — and the proof obligation marker `⊣`. They are proposals, not conclusions. The user validates, promotes, or discards them.

**Known open obligations (`⊣`):**
- Multi-connective sentence handling (currently takes the first match per sentence)
- Sentence boundary quality (trailing noise in object names)

---

## 5. The Cognitive Linter

**File:** `tools/cognitive_linter.py`
**Status:** `∃F+`
**Requires:** `pyyaml`

The only tool in the toolchain that reasons about time. Where the Validator checks grammar and the Linker checks referential integrity, the Cognitive Linter checks whether the user is following through on what they marked as important.

It reads `journal.log`, builds `Γ` incrementally across sessions, and flags labels that have stagnated beyond defined thresholds.

### 5.1 Staleness Thresholds

| Label type | Default threshold | Escalation behaviour |
| :---- | :---- | :---- |
| `!∄F` critical blocker | 1 session | `STAGNATION_ALERT` |
| `⊣` proof obligation | 3 sessions | Warning with resolution prompt |
| `?` heuristic label | 2 sessions | Warning with formalisation prompt |

Deferred items (explicitly acknowledged in the journal) receive doubled thresholds before re-escalating. A deferred `⊣` is still a `⊣` — deferral does not close an obligation.

### 5.2 Γ Construction

The Linter builds `Γ` by iterating sessions in chronological order:

- New subject → add to `Γ` with `sessions_open = 1`
- Existing subject, same completeness → increment `sessions_open`
- Existing subject, changed completeness → mark resolved, reset `sessions_open = 1`
- Subject in `deferred` block → set `deferred = True`, store reason

### 5.3 Rule F (Temporal)

The Linter performs temporal conflict detection across session boundaries — checking whether `A ⊢ B` and `A ⊢ ¬B` have been introduced in different sessions. This catches Epistemic Dissonance that snapshot tools cannot detect.

### 5.4 Resolution Prompts

Each flagged item generates a single actionable question keyed to its completeness state. These prompts are designed to feed directly into the opening of the next session, before the audit prompt runs.

### 5.5 Output

The Linter output mirrors the v2.7 audit prompt structure. Exit codes: 0 = velocity optimal, 1 = issues detected.

JSON output (`--json`) serialises the full `Γ` state and report for downstream consumption.

---

## 6. The Journal Manager

**File:** `tools/journal_manager.py`
**Status:** `∃F+`
**Requires:** `pyyaml`

Appends validated session label sets to `journal.log`. Validates each label before writing — invalid labels are silently excluded from the journal, ensuring the persistent record of `Γ` is always schema-compliant.

### 6.1 Journal Format

```yaml
---
session: 2026-03-18T10:00:00    # ISO 8601 timestamp
anchor: "Session anchor concept" # optional descriptive anchor
protocol: DETENTE                # operational state (DETENTE or AUFHEBEN)
gamma:
  - "~⊕∃F: Curry_Howard_Isomorphism"
  - "#⊕∃F: borrowBook ⊣"
deferred:                        # optional — explicitly acknowledged open items
  - subject: "borrowBook"
    reason: "waiting on type system decision"
---
```

`journal.log` is excluded from version control via `.gitignore`. It is a personal epistemic record, not a repository artefact.

---

## Inter-Tool Dependency Graph

```
journal.log
     │
     └── cognitive_linter.py
              │
              └── validate_label.py

journal_manager.py
     │
     └── validate_label.py

*.md files in repository
     │
     ├── linker.py
     │        └── validate_label.py
     │
     └── visualizer.py
              └── validate_label.py

raw text input
     │
     └── nlle_suggestor.py
```

---

## Open Proof Obligations

The following enhancements are identified but not yet implemented:

| Subject | Completeness | Description |
| :---- | :---- | :---- |
| `Linker_Fuzzy_Resolution` | `⊣` | Name aliasing — treat `Curry_Howard` and `Curry_Howard_Isomorphism` as the same subject |
| `Visualizer_Relation_Styling` | `⊣` | Distinct edge colours per relation type (`⊢` vs `≅` vs `⊂`) |
| `Visualizer_Node_Colouring` | `⊣` | Node fill colour keyed to completeness state |
| `Visualizer_Example_Filter` | `⊣` | Exclude labels in documentation example files from the graph |
| `NLLE_Multi_Connective` | `⊣` | Handle sentences containing more than one connective pattern |

---

*This document is part of the Strategic Labelling Framework repository.*
*See also: tools/README.md, schema.md, extensions/operational_semantics.md*
