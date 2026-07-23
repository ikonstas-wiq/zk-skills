---
name: cleanup-pr
description: Finish repository cleanup after a pull request has merged. Use when asked to clean up, close out, or finish merged work by verifying the merge, deleting the exact remote and local feature branches, closing resolved GitHub issues, applying only documentation updates already identified during the session, scanning nearby open issues for material impact, and reporting the final state. Do not use before the pull request is merged or for general issue triage.
---

# Clean up a merged PR

Complete the operational loose ends from one merged pull request without disturbing unrelated branches, issues, documentation, or worktree changes.

## 1. Resolve the exact scope

Read repository instructions and inspect the worktree before changing anything. Use local `git` for branches and `gh` for GitHub state.

Resolve the pull request from the user's number or URL, the current branch, or the most recently merged PR only when that inference is unambiguous. Record:

- repository owner and name
- PR number, title, URL, merge state, and merge time
- base branch and exact PR head branch
- PR head SHA and head repository
- issues GitHub marks as closing references

Confirm the PR is merged. If it is open, closed without merge, or ambiguous, stop and report the mismatch. Never reinterpret “cleanup” as permission to merge it.

Inspect the branch and worktree before deletion. Preserve unrelated changes. Never delete a default branch, protected branch, branch used by another open PR, or a branch whose current tip has advanced beyond the merged PR head.

## 2. Reconcile known documentation

Treat documentation as a bounded check, not a repository-wide hunt.

- If documentation or a specific Markdown file was raised earlier in the session, inspect only those known files and confirm the merged result reflects the completed work.
- If those files are stale, make the smallest local update and run any relevant documentation check.
- If documentation was not raised during the session and the PR does not contain an explicit documentation follow-up, record `Skipped — no known documentation follow-up` and do not search broadly for possible docs.

Do not discard or strand a required documentation update just to finish branch deletion. If a newly discovered edit still needs its own commit or pull request, preserve it on an appropriate follow-up branch and report that cleanup remains partially complete. Do not silently push or open a new PR unless the user authorized that work.

## 3. Close resolved issues

Start with GitHub's closing references and explicit issue references in the PR body, commits, and discussion. Inspect each candidate issue before changing it.

Close an issue as `completed` only when the merged PR satisfies the issue's requested outcome. Leave parent trackers, partially implemented issues, follow-up work, and merely related issues open. When closing manually, add a concise comment linking the merged PR unless that relationship is already clear in the issue timeline.

Verify the final state of every directly resolved issue. Do not assume GitHub auto-closed an issue, because merges into non-default branches and non-closing keywords can leave it open.

## 4. Scan affected open issues

Perform a quick, targeted scan rather than a full backlog triage:

1. Derive a few distinctive terms, labels, components, or file areas from the PR.
2. Search open issues in this repository for those signals and for references to the resolved issues.
3. Inspect only plausible matches.
4. Update an issue only when the merge materially changes its status, assumptions, dependency order, or remaining scope.

Close a matched issue only if it is fully resolved. Otherwise leave it open and, when useful, add one concise comment stating what the merged PR changed and what remains. Avoid low-information comments and duplicate updates.

## 5. Delete the merged branches safely

Handle the remote and local branch independently and verify both outcomes.

### Remote branch

Resolve the remote that corresponds to the PR head repository. Before deletion:

- confirm the exact remote branch still exists
- confirm its tip still matches the recorded PR head SHA
- confirm no open PR now uses that branch
- confirm it is not the default or a protected branch

Delete only that exact remote ref. If GitHub already deleted it, treat the remote cleanup as complete. If the branch has advanced, belongs to an external fork, or cannot be resolved safely, do not delete it; report the blocker and the observed SHAs.

### Local branch

If currently on the merged branch, first switch to the PR base or repository default branch. Fetch and update that destination using the repository's documented safe method; prefer a fast-forward-only pull.

Before deletion, compare the local tip with the recorded PR head SHA. If the local branch has commits that were not in the merged PR, preserve it and report them. Otherwise try safe deletion with `git branch -d`. A squash or rebase merge may make the safe ancestry check fail; use force deletion only after independently confirming all of the following:

- the PR is merged
- the local tip is exactly the recorded PR head SHA
- the branch has no additional local commits
- the worktree does not depend on the branch

Never use a broad branch pattern or delete unrelated stale branches.

## 6. Verify and report

Re-query state after the mutations. Confirm:

- the PR remains merged
- the exact remote branch is absent
- the exact local branch is absent
- directly resolved issues are closed
- related open issues received only necessary updates
- known documentation is current, explicitly skipped, or preserved as a named follow-up
- unrelated worktree changes remain intact

Return a compact checklist table:

| Area | Result | Evidence or follow-up |
| --- | --- | --- |
| Pull request | Merged | PR link and merge time |
| Remote branch | Deleted / already absent / blocked | Exact remote ref |
| Local branch | Deleted / already absent / blocked | Exact local ref |
| Resolved issues | Closed / none / blocked | Issue links |
| Related issues | Updated / no material matches | Issue links and one-line impact |
| Documentation | Updated / verified / skipped / follow-up | Exact paths |

Call cleanup complete only when both branch refs are absent and every confirmed resolved issue is closed. Distinguish already-clean state from work performed during the run.
