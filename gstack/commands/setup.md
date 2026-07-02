---
description: "One-time setup: install the pinned gstack runtime so /speckit.gstack.* commands work (integration-agnostic)."
---

# gstack setup

Installs the [gstack](https://github.com/garrytan/gstack) runtime (shared `bin/`, `scripts/`, `lib/`
and every skill directory) at `~/.gstack/runtime` — a neutral, **integration-agnostic**
home that works whether Spec Kit is wired to Copilot, Codex, Cursor, Claude, or
anything else. (gstack normally bakes the Claude-specific `~/.claude/skills/gstack`
path into its skills; this extension rewrites those references to
`~/.gstack/runtime` and exports `GSTACK_DIR` so the relocatable runtime resolves
correctly.)

Run this **once** before using any other `/speckit.gstack.*` command, and again
after updating the extension.

Pinned to gstack `v1.58.5.0` (commit `11de390be1be6849eb9a15f91ff4922dd16c589a`).

## Steps

1. Provision the runtime at the neutral home, pinned to the matching commit:

   ```bash
   GSTACK_SHA="11de390be1be6849eb9a15f91ff4922dd16c589a"
   DEST="$HOME/.gstack/runtime"
   mkdir -p "$(dirname "$DEST")"
   if [ -d "$DEST/.git" ]; then
     git -C "$DEST" fetch --depth 1 origin "$GSTACK_SHA"
   else
     rm -rf "$DEST"
     git init -q "$DEST"
     git -C "$DEST" remote add origin https://github.com/garrytan/gstack.git
     git -C "$DEST" fetch --depth 1 origin "$GSTACK_SHA"
   fi
   git -C "$DEST" checkout -q --force FETCH_HEAD
   chmod +x "$DEST"/bin/* 2>/dev/null || true
   ```

2. Export `GSTACK_DIR` and add the runtime to `PATH`, for this and future shells:

   ```bash
   printf 'export GSTACK_DIR="%s"\n' "$HOME/.gstack/runtime" >> "$HOME/.profile"
   printf 'export PATH="%s/bin:$PATH"\n' "$HOME/.gstack/runtime" >> "$HOME/.profile"
   export GSTACK_DIR="$HOME/.gstack/runtime"
   export PATH="$HOME/.gstack/runtime/bin:$PATH"
   ```

3. **Optional (recommended for browser/design skills):** run gstack's own
   installer, which builds the `browse`/`design` binaries. Requires
   [`bun`](https://bun.sh):

   ```bash
   if command -v bun >/dev/null 2>&1; then
     (cd "$HOME/.gstack/runtime" && ./setup)
   else
     echo "bun not installed — core (bash) skills work; browse/design/scrape need bun."
   fi
   ```

4. Verify:

   ```bash
   ls "$HOME/.gstack/runtime/bin/gstack-config" && echo "gstack runtime ready"
   ```

If anything fails, confirm `git` (and optionally `bun`) are installed and that
`$HOME/.gstack/` is writable.
