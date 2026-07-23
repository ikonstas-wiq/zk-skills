---
name: triage-git-issues
description: Scan and triage a GitHub repository's existing open issues into an implementation-ready backlog. Use when asked to review GitHub issues, recap their intent, identify duplicates or dependencies, recommend sequencing, estimate agent readiness versus grooming needs, assign low/medium/high effort, or return an issue triage table. Keep the workflow read-only unless the user explicitly asks to edit, label, close, or comment on issues.
---

# Triage GitHub issues

Build an evidence-backed view of the open backlog: what each issue asks for, what should happen first, and which items an implementation agent can start without product or technical clarification.

## 1. Set the repository and scope

Read repository instructions and use `gh` to confirm the repository owner, name, and default branch. Default to all open issues in the current project repository. Honor narrower filters from the user, such as a label, milestone, component, or issue range.

Fetch enough fields to scan the backlog efficiently: number, title, body, labels, assignees, milestone, creation and update times, comments, and URL. If the repository has more issues than one request returns, paginate or divide the query. State any deliberate limit rather than implying complete coverage.

Keep triage read-only. Do not comment, label, assign, close, reopen, or edit issues unless the user explicitly requests those mutations.

## 2. Understand each issue

Read the complete issue body and relevant recent comments. Inspect linked pull requests, referenced issues, specifications, or repository files only as needed to judge scope and readiness.

Write a one-sentence recap that states the requested outcome rather than repeating the title. Flag:

- likely duplicates or superseded requests
- missing reproduction, acceptance criteria, or expected behavior
- unresolved product, architecture, security, data, or compatibility decisions
- stale assumptions contradicted by the current repository
- work that should be split because it contains independently deliverable outcomes

Separate evidence from inference. When a dependency is inferred from overlapping components rather than explicitly recorded, label it as inferred.

## 3. Determine dependencies and sequence

Build a dependency graph from explicit blockers, shared foundations, migrations, API contracts, and overlapping ownership. Avoid inventing a sequence merely because issue numbers or creation dates differ.

Assign one sequencing recommendation to each issue:

- `Now`: no known prerequisite; suitable for the next implementation batch
- `After #N`: depends on a named issue or foundational change
- `Parallel`: independent and safe to implement alongside named work
- `Blocked`: requires an external decision, access, reproduction, or upstream change
- `Split first`: contains multiple outcomes that should be groomed separately
- `Duplicate of #N`: do not implement independently

When two issues conflict, describe the decision needed instead of selecting one without evidence. Recommend a practical order that minimizes rework and exposes risky assumptions early.

## 4. Rate agent readiness

Judge whether a fresh implementation agent could make a correct, bounded change and verify it without guessing at material requirements.

Use these ratings:

| Rating | Meaning |
| --- | --- |
| `Ready` | Outcome, scope, constraints, and verification are sufficiently clear; no unresolved dependency blocks work. |
| `Light grooming` | Implementable after a small factual clarification or acceptance-criteria addition. |
| `Needs grooming` | Material behavior, scope, reproduction, design, or verification details are missing. |
| `Blocked` | A dependency, decision, access requirement, or external event prevents implementation. |

Do not mark an issue ready merely because it is short. Require a testable outcome, enough repository context to locate the change, and no unresolved choice that could produce substantially different implementations.

For every non-ready issue, state the smallest concrete grooming action that would raise its readiness. Prefer a question that can be answered or an artifact that can be added over a vague request for “more detail.”

## 5. Estimate effort

Assign a coarse implementation effort that includes code, tests, and likely review fixes:

- `L`: localized, understood change with focused verification and little coordination
- `M`: multi-file or interface change, moderate uncertainty, migration work, or several focused test cases
- `H`: architectural or cross-system change, high uncertainty or risk, extensive migration/compatibility work, or an issue that should probably be split

Treat effort as an estimate, not elapsed time. Do not let missing requirements masquerade as high effort; mark the readiness gap separately and qualify the estimate when grooming could change it substantially.

## 6. Return the triage table

Lead with two or three concise observations about backlog shape, dependency bottlenecks, duplicates, or the best starting batch. Then return every issue in scope in a Markdown table sorted by recommended implementation order, then dependency chain, then issue number.

Use this schema:

| Order | Issue | Recap | Dependencies / sequence | Agent readiness | Effort | Grooming or implementation note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [#123](URL) Title | Requested outcome | Now | Ready | L | Focused first step or verification target |

Keep recaps and notes compact enough that the table remains scannable. Link every issue. Use stable issue numbers in dependency references.

After the table, list:

- assumptions and inferred dependencies
- issues excluded by filters or access limits
- the recommended first implementation batch

Do not convert the triage into tickets, edit GitHub, or begin implementation unless the user asks for that follow-up.
