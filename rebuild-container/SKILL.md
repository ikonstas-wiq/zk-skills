---
name: rebuild-container
version: 1.0.0
description: "Health check for devcontainer: verifies core productivity tools, MCP servers, skill symlinks, and auth status."
user_invocable: true
metadata:
  openclaw:
    category: "devops"
---

# Rebuild Container Health Check

Run a comprehensive health check on the devcontainer to verify all core productivity tools, MCP servers, and skill symlinks are in place.

## Instructions

When this skill is invoked, run ALL of the following checks and present results in a single summary table. Fix issues automatically where possible; flag manual steps (e.g. browser-based OAuth) for the user.

### 1. Core CLI Tools

Check each tool is installed, on PATH, and authenticated:

| Tool | Binary | Install method | Auth check command | Install command |
|------|--------|----------------|--------------------|-----------------|
| **gws** | `gws` | `npm install -g @googleworkspace/cli` | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/workspace/gws-cli-setup/.config gws auth status` — check `token_valid: true` | `npm install -g @googleworkspace/cli` |
| **msgraph** | `msgraph` (in venv) | editable install in `/workspace/msgraph-cli/.venv` | `source /workspace/msgraph-cli/.venv/bin/activate && msgraph auth status` — check `authenticated: true` | `cd /workspace/msgraph-cli && rm -rf .venv && UV_EXTRA_INDEX_URL="" uv venv --python $(which python3) .venv && UV_EXTRA_INDEX_URL="" uv pip install -e .` |
| **acli** | `acli` | Homebrew (`brew install acli`) at `/home/linuxbrew/.linuxbrew/bin/acli` | `source /workspace/atlassian-cli/scripts/start-acli-session.sh && acli auth status` | Install Homebrew first if missing (see §1a), then `brew tap atlassian/homebrew-acli && brew install acli` |
| **agents-cli** | `agents-cli` | `uv tool install` into `/workspace/.uv-tools` (persistent) | `agents-cli login --status` — check `Authenticated as ...` | `UV_TOOL_DIR=/workspace/.uv-tools UV_TOOL_BIN_DIR=/workspace/.uv-tools/bin UV_EXTRA_INDEX_URL="" uv tool install google-agents-cli`. Auth piggybacks on existing `gcloud` ADC — no separate login needed if `gcloud auth list` shows an active account |

For each tool:
1. Check if binary exists / is on PATH
2. If missing, attempt auto-install (gws, msgraph, **and** acli — install Homebrew first if needed)
3. Check auth status
4. If not authenticated, tell user the exact command to run interactively (auth requires browser)

#### 1a. System Dependencies (apt)

acli requires `dbus-x11`, `gnome-keyring`, and `xdg-utils` for token storage and browser launch. Check if they're installed and install if missing:

```bash
# Check
for pkg in dbus-x11 gnome-keyring xdg-utils; do
  dpkg -l "$pkg" 2>/dev/null | grep -q '^ii' || NEEDS_APT=true
done

# Install if missing — requires sudo (flag for user if Claude can't run it)
if [ "$NEEDS_APT" = true ]; then
  sudo apt-get update -qq && sudo apt-get install -y -qq dbus-x11 gnome-keyring xdg-utils
fi
```

**Note:** Claude Code typically cannot run `sudo`. If apt install fails, tell the user to run it manually in VS Code terminal.

#### 1b. Homebrew Auto-Install

If `brew` is not found at `/home/linuxbrew/.linuxbrew/bin/brew`, install it non-interactively:

```bash
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

Then install acli:
```bash
brew tap atlassian/homebrew-acli && brew install acli
```

**Important env vars that must be set for commands to work:**
- `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/workspace/gws-cli-setup/.config` (for gws)
- msgraph must be run inside its venv: `source /workspace/msgraph-cli/.venv/bin/activate`
- acli needs D-Bus session: `source /workspace/atlassian-cli/scripts/start-acli-session.sh`
- agents-cli needs `/workspace/.uv-tools/bin` on PATH (set in `~/.zshrc`)

### 2. MCP Servers

Check which MCP servers are currently connected to the session. Use the system-reminder at the top of the conversation that lists available deferred tools — tools prefixed with `mcp__` indicate active MCP servers.

Look for these expected MCP servers:
- **Playwright** (`mcp__playwright__*`) — browser automation
- **Slack** (`mcp__claude_ai_Slack__*`) — Slack integration
- **Microsoft 365** (`mcp__claude_ai_Microsoft_365__*`) — Outlook integration via cloud connector

Report which are connected and which are missing. MCP servers are managed by the Claude Code host (VS Code / desktop app), not the container itself — so if one is missing, tell the user to check their MCP config in the host app rather than trying to fix it inside the container.

### 3. Skill Symlinks

Verify all expected skill families are symlinked into `~/.claude/skills/`:

| Family | Source | Expected pattern | Symlink command |
|--------|--------|------------------|-----------------|
| **gws** | `/workspace/google-cli/skills/gws-*` | `gws-*` (shared, calendar, gmail, drive, docs, sheets, slides, etc.) | `for s in /workspace/google-cli/skills/gws-*; do ln -sfn "$s" ~/.claude/skills/$(basename "$s"); done` |
| **acli** | `/workspace/atlassian-cli/skills/acli-*` and `recipe-*` | `acli-*`, `recipe-*` | `for s in /workspace/atlassian-cli/skills/*/; do ln -sfn "$s" ~/.claude/skills/$(basename "$s"); done` |
| **msgraph** | `/workspace/msgraph-cli/skills/msgraph-*` | `msgraph-*` (shared, mail, calendar) | `for s in /workspace/msgraph-cli/skills/msgraph-*; do ln -sfn "$s" ~/.claude/skills/$(basename "$s"); done` |
| **agents-cli** | `/workspace/google-agents-cli/skills/google-agents-cli-*` | `google-agents-cli-*` (workflow, adk-code, scaffold, eval, deploy, publish, observability) | `for s in /workspace/google-agents-cli/skills/google-agents-cli-*; do ln -sfn "$s" ~/.claude/skills/$(basename "$s"); done` |
| **custom** | Direct dirs in `~/.claude/skills/` | `custom-gws-docs-format`, `custom-gws-gmail-format`, `custom-gws-slides-edit` | N/A — created manually |
| **zk** | Direct dirs in `~/.claude/skills/` | `zk-write-guide`, `zk-leadership-guide` | N/A — created manually |

For each family:
1. Check source directory exists
2. Check symlinks exist and point to valid targets (not broken)
3. If symlinks are broken or missing, re-create them automatically
4. Report count of skills per family

### 4. Environment Variables

Verify these are set (check both current env and `~/.zshrc`):

- `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` → should be `/workspace/gws-cli-setup/.config`
- `PATH` should include `/home/linuxbrew/.linuxbrew/bin` (for acli)
- `MSGRAPH_CLIENT_ID` and `MSGRAPH_TENANT_ID` → should be set (check `/workspace/msgraph-cli/.env`)
- `UV_TOOL_DIR=/workspace/.uv-tools`, `UV_TOOL_BIN_DIR=/workspace/.uv-tools/bin`, and PATH should include `/workspace/.uv-tools/bin` (for agents-cli)

#### 4a. Auto-fix .zshrc

If any of the following are missing from `~/.zshrc`, **append them automatically**:

```bash
# Google Workspace CLI config directory
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/workspace/gws-cli-setup/.config

# Homebrew (for acli)
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" 2>/dev/null

# uv tool storage on /workspace so installs survive container rebuilds
export UV_TOOL_DIR=/workspace/.uv-tools
export UV_TOOL_BIN_DIR=/workspace/.uv-tools/bin
export PATH="/workspace/.uv-tools/bin:$PATH"
```

Check with `grep` before appending to avoid duplicates.

### 5. Output Format

Present results as a summary table:

```
## Container Health Check

| Category | Item | Status | Action |
|----------|------|--------|--------|
| CLI | gws | OK / MISSING / NO AUTH | ... |
| CLI | msgraph | OK / MISSING / NO AUTH | ... |
| CLI | acli | OK / MISSING / NO AUTH | ... |
| CLI | agents-cli | OK / MISSING / NO AUTH | ... |
| MCP | Playwright | CONNECTED / MISSING | ... |
| MCP | Slack | CONNECTED / MISSING | ... |
| MCP | Microsoft 365 | CONNECTED / MISSING | ... |
| Skills | gws (N) | OK / BROKEN | ... |
| Skills | acli (N) | OK / BROKEN | ... |
| Skills | msgraph (N) | OK / BROKEN | ... |
| Skills | agents-cli (N) | OK / BROKEN | ... |
| Env | GWS config dir | OK / MISSING | ... |
| Env | Brew PATH | OK / MISSING | ... |

### Manual Steps Required
- (list any auth commands user needs to run interactively)
```

Auto-fix what you can (install CLIs, re-symlink skills, set env vars). Flag what requires user action (OAuth logins, brew installs, MCP config).

### 6. Playwright (Browser & PDF Generation)

Playwright is used for two purposes: (a) the Playwright MCP server for browser automation/QA, and (b) the Playwright npm library for HTML-to-PDF generation.

#### 6a. Install Playwright library + system deps

Run these four commands in sequence. Requires `sudo` — if Claude cannot run them, tell the user to run in VS Code terminal:

```bash
sudo -E npm install -g @playwright/test @playwright/mcp && \
sudo -E npx playwright install-deps && \
node /usr/local/lib/node_modules/@playwright/mcp/node_modules/playwright/cli.js install chromium && \
sudo chown -R node:node /home/node/{.npm,.cache/ms-playwright,.pki/nssdb}
```

This installs the Playwright npm packages globally, installs all required system libraries (libnspr4, libnss3, libasound2, GTK, GStreamer, etc.), downloads Chromium, and fixes file ownership.

**Verify** after install:
```bash
NODE_PATH=/home/node/.npm-global/lib/node_modules node -e "const { chromium } = require('playwright'); console.log('Playwright library OK');"
```

#### 6b. Register Playwright MCP server

The user must run this command in their **host terminal** (not inside the container), as MCP server config is managed by the Claude Code host app:

```bash
claude mcp add playwright -- npx @playwright/mcp --browser chromium --no-sandbox --isolated --headless
```

After adding, restart Claude Code for the MCP server to appear in the session.

Include in the summary table as:

```
| Playwright | Library | OK / MISSING | Run install command (sudo) |
| Playwright | MCP Server | CONNECTED / MISSING | User: run `claude mcp add` on host |
```

### 7. Port Forwarding (devcontainer.json)

acli's OAuth flow starts a local HTTP server on a random high port (32768-65535) for the callback. The devcontainer must forward these ports to the host for the browser redirect to reach the container.

Check if the active devcontainer.json includes port forwarding for high ports. Look for the config in common locations:
- `/workspace/.devcontainer/devcontainer.json`
- `/workspace/*/.devcontainer/devcontainer.json` (project subdirectories)

If `forwardPorts` is missing or doesn't cover the high port range, flag it as a manual step and tell the user to add this to their devcontainer.json:

```json
"forwardPorts": ["32768-65535"],
"portsAttributes": {
  "32768-65535": {
    "label": "OAuth callbacks",
    "onAutoForward": "silent"
  }
}
```

After adding, the container must be rebuilt for the change to take effect. Include this in the summary table as:

```
| Ports | OAuth callback (32768-65535) | OK / MISSING | Add forwardPorts to devcontainer.json |
```

**This is required for `acli auth login` to work in the container.** Without it, the OAuth callback cannot reach acli's local server and auth will fail with "authentication failed".
