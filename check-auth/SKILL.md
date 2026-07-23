---
name: check-auth
description: Check authentication status across all CLI tools (gws, msgraph, acli)
user_invocable: true
---

# Check Auth

Run authentication status checks for all three CLI services and present results in a summary table. For any service that is not authenticated, provide the exact interactive login command.

## Instructions

Run ALL three checks in parallel using the Bash tool, then present results.

### 1. gws (Google Workspace)

```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/workspace/gws-cli-setup/.config gws auth status 2>&1
```

- Look for `"token_valid": true` in the JSON output
- If authenticated, report the `user` field
- If not authenticated or binary missing, flag it

### 2. msgraph (Microsoft Graph / Outlook)

```bash
source /workspace/msgraph-cli/.venv/bin/activate && msgraph auth status 2>&1
```

- Look for `"authenticated": true` in the JSON output
- If not authenticated, flag it

### 3. acli (Atlassian / Jira / Confluence)

```bash
source /workspace/atlassian-cli/scripts/start-acli-session.sh 2>/dev/null && acli auth status 2>&1
```

- If `acli` is not on PATH, try with brew prefix: `eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && source /workspace/atlassian-cli/scripts/start-acli-session.sh 2>/dev/null && acli auth status 2>&1`
- Success = no error output
- If you see `unauthorized` or `use 'acli auth login'`, flag it

## Output Format

Present a compact table:

```
| Service | Status | User / Detail |
|---------|--------|---------------|
| gws     | OK / NO AUTH / MISSING | user@domain or error |
| msgraph | OK / NO AUTH / MISSING | detail |
| acli    | OK / NO AUTH / MISSING | detail |
```

### Login Commands

For any service showing NO AUTH, provide the exact command the user should run interactively with the `!` prefix:

- **gws**: `! GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/workspace/gws-cli-setup/.config gws auth login`
- **msgraph**: `! source /workspace/msgraph-cli/.venv/bin/activate && msgraph auth login`
- **acli**: `! source /workspace/atlassian-cli/scripts/start-acli-session.sh && acli auth login`

If all three are authenticated, just say "All services authenticated" with the summary table.
