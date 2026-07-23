---
name: audit-pr-merge-readiness
description: Audit a large, stacked, or release-sensitive pull request change for merge readiness. Pin every PR boundary, run Matt Pocock's independent Standards and Spec review for each slice, verify high-risk public behavior through targeted execution, consolidate cross-PR findings with evidence and ownership, and produce a read-only merge recommendation. Use for dependent PR stacks, large multi-surface PRs, packaging or release changes, and requests for an evidence-backed merge gate. Use the ordinary code-review skill for a small single diff. Do not use this skill to implement fixes, comment on PRs, rebase, merge, or push.
---

# Audit PR merge readiness

Produce a read-only merge decision for a large change or dependent PR stack. Preserve the independent Standards and Spec reports, then add direct execution evidence and a stack-level finding ledger.

## Set the boundary

Treat the audit as read-only. Do not edit source, post comments, change PR state, commit, rebase, merge, or push. Temporary reproductions may write only outside the repository and must be removed after use.

Use this skill when at least one condition holds:

- Two or more PRs depend on one another.
- One PR crosses several public surfaces or release stages.
- The change affects packaging, installation, persistence, permissions, upgrades, rollback, or destructive behavior.
- The user asks for a merge gate backed by more than static diff inspection.

Route a small, ordinary single-diff review directly to `mattpocock-skills:code-review`.

## 1. Pin the review graph

Read repository guidance and preserve unrelated worktree changes. Fetch remote state only when the user requested current PR information or the local refs are stale.

For every PR, record:

- PR number, title, declared base, head branch, and exact head SHA
- current target-base head SHA at audit time
- merge-base SHA between the target-base head and PR head
- commit list
- diff command
- CI and merge state at review time

Model a stack as ordered slices. Compare each PR with its immediate parent rather than comparing every head with the default branch. Use the merge base to isolate the PR's introduced diff. Use the current target-base head to judge merge readiness.

If the current target-base head is not an ancestor of the PR head, record the divergence and test whether the live merge conflicts. Do not substitute the older merge base for the current merge target. Confirm that declared bases and actual ancestry agree before continuing.

Fail early on an unresolved ref, empty slice, ambiguous stack order, or dirty path that overlaps the audit.

## 2. Build the claims and evidence plan

Read the issue, PR descriptions, specifications, release notes, manifests, and operator documentation that define the change. Turn material claims into an evidence table:

| Field | Meaning |
| --- | --- |
| Claim | Observable behavior or release promise |
| Owner | PR slice that introduces it |
| Public surface | Interface through which a user or operator observes it |
| Static evidence | Relevant diff, contract, test, manifest, or documentation |
| Executable check | Focused command, reproduction, or packaged-artifact test |
| Result | Confirmed, contradicted, deferred, or unverified |

Prioritise boundaries where a green unit suite can miss the delivered behavior:

- wire formats, exit codes, headers, and error contracts
- persisted data, migrations, ordering, and pagination
- packaged, installed, generated, or published artifacts
- filesystem aliases, cross-platform behavior, and environment discovery
- retry, upgrade, rollback, idempotency, and partial failure
- authentication, authorization, destructive operations, and custody

Keep deferred external gates separate from code defects. Do not invent evidence for access that is unavailable.

## 3. Run the independent review axes

Invoke `mattpocock-skills:code-review` separately for every pinned slice. Supply that slice's merge-base fixed point, commit list, and resolved spec sources. Pass the exact spec paths or fetched contents so delegated reviewers do not need to rediscover or refetch them.

Run one slice's Standards and Spec pair at a time. A stack costs two delegated reviews per slice; state that scope before starting when the stack has more than two slices. If a delegated pass stalls or cannot access its source, stop that pass, mark the axis incomplete, and continue gathering direct evidence. Do not wait indefinitely or silently replace the missing axis with the primary agent's opinion. An incomplete required axis prevents a `Ready` verdict.

Retain the Standards and Spec results as separate source reports. Do not rewrite their priorities or combine their counts. Record their findings in the stack ledger with provenance so later synthesis can deduplicate overlap without altering either axis.

## 4. Verify high-risk claims

Use the smallest public-facing check that can confirm or contradict each material claim.

Start with focused existing tests. Add direct execution when static tests do not exercise the delivered boundary. Examples include installing the packed artifact in a temporary prefix, invoking the public CLI, inspecting an archive manifest, replaying an upgrade, or reproducing a filesystem topology in a temporary home.

For each check, capture:

- exact command or setup
- expected observable result
- actual result and exit status
- environment or platform limits
- whether the check used source files or the delivered artifact

Create a temporary reproduction only when the behavior remains uncertain. Keep it minimal, avoid credentials and personal data, and do not turn review-only code into a repository change.

Run broad test suites only after focused checks when their cost is reasonable. A passing broad suite does not override a failing public-surface reproduction.

## 5. Consolidate the finding ledger

Deduplicate findings across PR slices and review sources. Assign every consolidated finding to the earliest PR that introduced it.

Record:

- stable finding ID and owner PR
- priority and affected quality: effectiveness, simplicity, or maintainability
- Standards, Spec, or direct-verification provenance
- concrete evidence and reproduction result
- user, operator, release, or maintenance impact
- smallest coherent fix
- confidence and any unverified assumption

Use these priorities:

- `P0`: active security exposure, data loss, or unrecoverable corruption
- `P1`: merge blocker affecting promised public behavior, legal compliance, release viability, or safe operation
- `P2`: required correctness, consistency, upgrade safety, or material maintainability work
- `P3`: worthwhile non-blocking improvement

Do not use decimal quality scores. Explain the observed strength or weakness instead.

## 6. Decide merge readiness

Choose one verdict and state the evidence behind it:

- `Hold`: any unresolved P0 or P1, or a material high-risk claim that could not be verified
- `Changes required`: no P0/P1, but unresolved P2 work contradicts the stated behavior or safe merge order
- `Ready`: no unresolved merge blocker and the evidence covers the delivered public surfaces

For a stack, state:

- which PR owns each gate
- required fix and merge order
- whether a base change requires restacking descendants
- which checks must rerun after the base changes

Do not treat green CI as proof for behavior the workflow does not exercise.

## 7. Report

Return concise Markdown by default. Include exact refs, verdict, findings ordered by merge impact, positive evidence, commands run, and limits.

When the user requests a visual or shareable report, prepare traceable Markdown source topics and invoke `mds-to-html`. A useful tab plan is Executive, one tab per PR, Findings, and Evidence. Let `mds-to-html` and `design-system` own layout, accessibility, responsive behavior, and visual review.

Keep the two Matt review axes visible in the Evidence section. Label the consolidated action list as a separate synthesis informed by those axes and direct verification.

Stop after the report. Route implementation to an implementation skill and GitHub mutations to the relevant GitHub skill.

## Completion checks

Before reporting, confirm:

- Every PR slice uses its immediate parent and pinned SHAs.
- Current target-base heads and historical merge bases are recorded separately.
- Every material claim has evidence or an explicit unverified status.
- High-risk delivered artifacts were checked as artifacts when practical.
- Findings are deduplicated and assigned to one owner PR.
- Standards and Spec reports remain independently attributable.
- Deferred external gates are not reported as code defects.
- The verdict follows from the unresolved priorities and evidence.
- No repository or GitHub state changed during the audit.
