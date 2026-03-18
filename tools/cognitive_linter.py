#!/usr/bin/env python3
"""
Strategic Labelling Framework — Cognitive Linter v1.1

Monitors epistemic velocity across sessions by reading journal.log
and flagging labels that have stagnated beyond defined thresholds.

The Linter is the only tool in the SLF toolchain that reasons about
*time*. Where the Validator checks grammar and the Linker checks
referential integrity, the Linter checks whether the user is following
through on what they said mattered.

This is the framework applying its own epistemic honesty principle to
the user's behaviour — not just to the labels themselves.

Usage:
    python cognitive_linter.py                    # reads journal.log
    python cognitive_linter.py path/to/journal.log
    python cognitive_linter.py --json

Requires: pyyaml (pip install pyyaml)
"""

import sys
import json
import yaml
from dataclasses import dataclass, field
from typing import Optional
from validate_label import validate_label

# ── Thresholds ────────────────────────────────────────────────────────────────
# These match docs/toolchain_specification.md §2.1 (v2.8-alpha)
THRESHOLDS = {
    'CRITICAL_BLOCKER': 1,   # !∄F must transition within 1 session
    'STALE_OBLIGATION': 3,   # ⊣   must transition within 3 sessions
    'HEURISTIC_DECAY':  2,   # ?   must be formalised within 2 sessions
}

DEFAULT_LOG = "journal.log"

# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class TrackedLabel:
    """A label as it exists across sessions in Γ."""
    subject:      str
    completeness: str
    intensity:    str
    uncertainty:  Optional[str]
    raw_label:    str
    first_seen:   str          # ISO session timestamp
    last_seen:    str
    sessions_open: int = 1
    resolved:     bool = False
    deferred:     bool = False
    deferred_reason: Optional[str] = None

@dataclass
class LintReport:
    """Structured output from a single linter run."""
    critical_stagnations: list = field(default_factory=list)
    stale_obligations:    list = field(default_factory=list)
    heuristic_decays:     list = field(default_factory=list)
    rule_f_violations:    list = field(default_factory=list)
    resolved_this_run:    list = field(default_factory=list)
    summary: dict         = field(default_factory=dict)

    def is_clean(self):
        return not any([
            self.critical_stagnations,
            self.stale_obligations,
            self.heuristic_decays,
            self.rule_f_violations,
        ])

# ── Journal parser ────────────────────────────────────────────────────────────

def load_journal(log_path: str) -> list[dict]:
    """
    Reads journal.log and returns a list of session entries in
    chronological order.

    Expected YAML format (as written by journal_manager.py):
        ---
        session: 2026-03-01T10:00:00
        anchor: "Setup"
        protocol: DETENTE
        gamma:
          - "~⊕∃F: Curry_Howard_Isomorphism"
          - "#⊕∃F: borrowBook ⊣"
        deferred:
          - subject: "borrowBook"
            reason: "waiting on type system decision"
        ---
    """
    sessions = []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"✗ Journal not found: {log_path}", file=sys.stderr)
        print("  Run journal_manager.py to create it.", file=sys.stderr)
        sys.exit(1)

    # Split on YAML document separators
    raw_docs = [d.strip() for d in content.split('---') if d.strip()]
    for doc in raw_docs:
        try:
            entry = yaml.safe_load(doc)
            if isinstance(entry, dict) and 'session' in entry:
                sessions.append(entry)
        except yaml.YAMLError:
            continue

    sessions.sort(key=lambda e: str(e.get('session', '')))
    return sessions

# ── Γ builder ─────────────────────────────────────────────────────────────────

def build_gamma(sessions: list[dict]) -> dict[str, TrackedLabel]:
    """
    Iterates sessions in order, building Γ incrementally.

    For each label in each session:
    - If the subject is new, add it to Γ with sessions_open = 1
    - If the subject already exists:
        - If the completeness has changed, mark resolved and reset counter
        - If unchanged, increment sessions_open
    - If the subject appears in the session's deferred list, mark deferred

    Returns: dict mapping subject name → TrackedLabel
    """
    gamma: dict[str, TrackedLabel] = {}

    for entry in sessions:
        session_id  = str(entry.get('session', 'unknown'))
        raw_labels  = entry.get('gamma', []) or []
        deferrals   = {d['subject']: d.get('reason') for d in (entry.get('deferred') or [])
                       if isinstance(d, dict) and 'subject' in d}

        for raw in raw_labels:
            if not isinstance(raw, str):
                continue
            res = validate_label(raw.strip())
            if not res.valid:
                continue

            subj       = res.parsed['subject']
            comp       = res.parsed['completeness']
            intensity  = res.parsed['intensity']
            uncertainty = res.parsed.get('uncertainty')

            if subj not in gamma:
                gamma[subj] = TrackedLabel(
                    subject=subj,
                    completeness=comp,
                    intensity=intensity,
                    uncertainty=uncertainty,
                    raw_label=raw.strip(),
                    first_seen=session_id,
                    last_seen=session_id,
                    sessions_open=1,
                )
            else:
                existing = gamma[subj]
                if comp != existing.completeness:
                    # State has transitioned — this is progress
                    existing.resolved = True
                    existing.completeness = comp
                    existing.intensity = intensity
                    existing.uncertainty = uncertainty
                    existing.raw_label = raw.strip()
                    existing.sessions_open = 1
                else:
                    existing.sessions_open += 1

                existing.last_seen = session_id

            # Apply deferral annotations
            if subj in deferrals:
                gamma[subj].deferred = True
                gamma[subj].deferred_reason = deferrals[subj]

    return gamma

# ── Rule F: temporal conflict detection ───────────────────────────────────────

def check_rule_f(sessions: list[dict]) -> list[str]:
    """
    Scans Γ for epistemic dissonance introduced across sessions.

    Contradiction: A ⊢ B and A ⊢ ¬B coexist in Γ.

    In practice this looks for subject-object pairs where the same
    subject appears with both a positive ⊢ and a negation marker
    toward the same object across the session history.

    This is a conservative heuristic; full negation detection would
    require natural language understanding beyond the label grammar.
    """
    violations = []
    # Map subject → set of (relation, object) pairs seen
    seen: dict[str, set] = {}

    for entry in sessions:
        session_id = str(entry.get('session', 'unknown'))
        for raw in (entry.get('gamma') or []):
            if not isinstance(raw, str):
                continue
            res = validate_label(raw.strip())
            if not res.valid:
                continue
            subj = res.parsed['subject']
            for rel, obj in zip(res.parsed['relations'], res.parsed['objects']):
                if obj is None:
                    continue
                key = (rel, obj)
                neg_key = (rel, f'NOT_{obj}')
                if subj not in seen:
                    seen[subj] = set()
                if neg_key in seen[subj]:
                    violations.append(
                        f"Rule F: '{subj}' has both '{rel} {obj}' and '{rel} NOT_{obj}' "
                        f"in Γ — Epistemic Dissonance detected (session: {session_id})"
                    )
                seen[subj].add(key)

    return violations

# ── Actionable prompts ────────────────────────────────────────────────────────

def resolution_prompt(tracked: TrackedLabel) -> str:
    """Generates a single precise question to unblock a stagnating label."""
    comp = tracked.completeness
    subj = tracked.subject.replace('_', ' ')

    if comp == '∄F':
        return f'→ "What specifically is missing from {subj}?"'
    if comp == '⊣':
        return f'→ "What is the next concrete step toward implementing {subj}?"'
    if tracked.uncertainty and '?' in tracked.uncertainty:
        return f'→ "What evidence would raise your confidence in {subj}?"'
    return f'→ "What would it take to advance {subj} to ∃F+?"'

# ── Core audit ────────────────────────────────────────────────────────────────

def run_audit(gamma: dict[str, TrackedLabel],
              rule_f_violations: list[str]) -> LintReport:
    """
    Applies staleness thresholds and collects findings into a LintReport.

    Deferred items are included in output as informational, not as warnings,
    unless they have been deferred past twice the original threshold —
    at which point they re-escalate. A deferred ⊣ is still a ⊣.
    """
    report = LintReport()

    for subj, tracked in gamma.items():
        comp      = tracked.completeness
        intensity = tracked.intensity
        n         = tracked.sessions_open
        deferred  = tracked.deferred

        # Skip closed items
        if comp == '∃F+':
            continue

        # Determine effective threshold (doubled if deferred)
        def threshold(base_key: str) -> int:
            t = THRESHOLDS[base_key]
            return t * 2 if deferred else t

        # Critical blocker: !∄F
        if intensity == '!' and comp == '∄F':
            if n > threshold('CRITICAL_BLOCKER'):
                report.critical_stagnations.append({
                    'subject': subj,
                    'sessions_open': n,
                    'first_seen': tracked.first_seen,
                    'deferred': deferred,
                    'deferred_reason': tracked.deferred_reason,
                    'prompt': resolution_prompt(tracked),
                    'label': tracked.raw_label,
                })

        # Stale proof obligation: ⊣
        elif comp == '⊣':
            if n > threshold('STALE_OBLIGATION'):
                report.stale_obligations.append({
                    'subject': subj,
                    'sessions_open': n,
                    'first_seen': tracked.first_seen,
                    'deferred': deferred,
                    'deferred_reason': tracked.deferred_reason,
                    'prompt': resolution_prompt(tracked),
                    'label': tracked.raw_label,
                })

        # Heuristic decay: ? uncertainty marker
        elif tracked.uncertainty and '?' in str(tracked.uncertainty):
            if n > threshold('HEURISTIC_DECAY'):
                report.heuristic_decays.append({
                    'subject': subj,
                    'sessions_open': n,
                    'first_seen': tracked.first_seen,
                    'deferred': deferred,
                    'prompt': resolution_prompt(tracked),
                    'label': tracked.raw_label,
                })

    report.rule_f_violations = rule_f_violations

    # Summary counts across all of Γ
    report.summary = {
        'total_tracked':        len(gamma),
        'obligations_open':     sum(1 for t in gamma.values() if t.completeness == '⊣'),
        'blockers_open':        sum(1 for t in gamma.values() if t.completeness == '∄F'),
        'partials_open':        sum(1 for t in gamma.values() if t.completeness == '∃f'),
        'complete':             sum(1 for t in gamma.values() if t.completeness == '∃F+'),
        'critical_stagnations': len(report.critical_stagnations),
        'stale_obligations':    len(report.stale_obligations),
        'heuristic_decays':     len(report.heuristic_decays),
        'rule_f_violations':    len(report.rule_f_violations),
        'conflict_status':      'Clear' if not report.rule_f_violations else 'DISSONANCE DETECTED',
    }

    return report

# ── Renderer ──────────────────────────────────────────────────────────────────

def render_report(report: LintReport):
    """Prints the audit report in a format that mirrors the v2.7 audit prompt."""
    print()
    print("─── SLF Cognitive Linter ─────────────────────────────────────────")
    print()

    if report.critical_stagnations:
        print("✗  CRITICAL STAGNATION  (!∄F unresolved past threshold)")
        for item in report.critical_stagnations:
            suffix = f"  [DEFERRED: {item['deferred_reason']}]" if item['deferred'] else ""
            print(f"   {item['label']}")
            print(f"   Sessions open: {item['sessions_open']}  |  First seen: {item['first_seen']}{suffix}")
            print(f"   {item['prompt']}")
            print()

    if report.stale_obligations:
        print("⚠  STALE PROOF OBLIGATIONS  (⊣ open past threshold)")
        for item in report.stale_obligations:
            suffix = f"  [DEFERRED: {item['deferred_reason']}]" if item['deferred'] else ""
            print(f"   {item['label']}")
            print(f"   Sessions open: {item['sessions_open']}  |  First seen: {item['first_seen']}{suffix}")
            print(f"   {item['prompt']}")
            print()

    if report.heuristic_decays:
        print("⚠  HEURISTIC DECAY  (? labels not formalised past threshold)")
        for item in report.heuristic_decays:
            print(f"   {item['label']}")
            print(f"   Sessions open: {item['sessions_open']}  |  First seen: {item['first_seen']}")
            print(f"   {item['prompt']}")
            print()

    if report.rule_f_violations:
        print("✗  EPISTEMIC DISSONANCE  (Rule F)")
        for v in report.rule_f_violations:
            print(f"   {v}")
        print()

    print("─── Γ Summary ────────────────────────────────────────────────────")
    s = report.summary
    print(f"   Total tracked:     {s['total_tracked']}")
    print(f"   ∃F+ complete:      {s['complete']}")
    print(f"   ⊣  obligations:    {s['obligations_open']}")
    print(f"   ∄F blockers:       {s['blockers_open']}")
    print(f"   ∃f partials:       {s['partials_open']}")
    print(f"   Conflict status:   {s['conflict_status']}")
    print()

    if report.is_clean():
        print("   Status: EPISTEMIC VELOCITY OPTIMAL")
    else:
        n = (s['critical_stagnations'] + s['stale_obligations']
             + s['heuristic_decays'] + s['rule_f_violations'])
        print(f"   Status: {n} issue(s) require attention")
        print()
        print("   Pass the flagged prompts above into your next session")
        print("   to prime blocker resolution before running the audit prompt.")

    print("──────────────────────────────────────────────────────────────────")
    print()

# ── Proof Search integration ──────────────────────────────────────────────────
try:
    from proof_search import run_for_linter
    flagged = []
    for item in report.critical_stagnations + report.stale_obligations:
        flagged.append({
            'subject':      item['subject'],
            'label':        item['label'],
            'prompt':       item['prompt'],
            'completeness': '∄F' if item in report.critical_stagnations else '⊣',
        })
    for item in report.heuristic_decays:
        flagged.append({
            'subject':      item['subject'],
            'label':        item['label'],
            'prompt':       item['prompt'],
            'completeness': '?',
        })
    if flagged:
        run_for_linter(flagged)
except ImportError:
    pass

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    log_path   = DEFAULT_LOG
    output_json = '--json' in sys.argv

    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            log_path = arg

    sessions       = load_journal(log_path)
    gamma          = build_gamma(sessions)
    rule_f         = check_rule_f(sessions)
    report         = run_audit(gamma, rule_f)

    if output_json:
        # Serialise TrackedLabel objects for JSON output
        gamma_serial = {
            k: {
                'subject':       v.subject,
                'completeness':  v.completeness,
                'intensity':     v.intensity,
                'sessions_open': v.sessions_open,
                'first_seen':    v.first_seen,
                'last_seen':     v.last_seen,
                'deferred':      v.deferred,
                'label':         v.raw_label,
            }
            for k, v in gamma.items()
        }
        output = {
            'gamma':   gamma_serial,
            'report':  {
                'critical_stagnations': report.critical_stagnations,
                'stale_obligations':    report.stale_obligations,
                'heuristic_decays':     report.heuristic_decays,
                'rule_f_violations':    report.rule_f_violations,
                'summary':              report.summary,
            }
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        render_report(report)

    sys.exit(0 if report.is_clean() else 1)
