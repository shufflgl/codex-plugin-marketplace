# My Codex Marketplace

A Codex Plugin Marketplace that can be distributed through Git. The marketplace
catalog is located at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json),
and plugin packages are located in [`plugins/`](plugins/). Every plugin includes
the required `.codex-plugin/plugin.json` manifest.
Allowed catalog categories are defined in [`categories.json`](categories.json).

The searchable web catalog is generated from those same repository sources by
[`plugin-marketplace-site/`](plugin-marketplace-site/) and published independently
on Cloudflare Pages at <https://codex-plugins.lglgl.me>.

## Validate Locally

```sh
python3 scripts/validate_marketplace.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Validate and export the website:

```sh
cd plugin-marketplace-site
bun install
bun run lint
bun run test
bun run build:pages
```

Temporarily add the marketplace from the local directory (this writes to your
Codex runtime configuration):

```sh
codex plugin marketplace add ./
codex plugin marketplace list
```

Then enter `/plugins` in Codex CLI, install a plugin from **My Codex Marketplace**,
and start a new session. Remove the local marketplace after testing:

```sh
codex plugin marketplace remove my-codex-marketplace
```

## Publish as a Git Marketplace

1. Initialize this directory and push it to GitHub, GitLab, or another accessible
   Git remote.
2. Users can add the marketplace in either of these ways:

   ```sh
   codex plugin marketplace add OWNER/REPOSITORY
   # Or pin to a branch or tag.
   codex plugin marketplace add OWNER/REPOSITORY --ref main
   ```

   Any Git URL can also be used:

   ```sh
   codex plugin marketplace add https://github.com/OWNER/REPOSITORY.git --ref main
   ```

3. Users can run `codex plugin marketplace upgrade my-codex-marketplace` to get
   later marketplace updates.

> For production use, pin `--ref` to a reviewed tag or commit SHA rather than
> continuously tracking a branch.

## Add a Plugin to This Repository

1. Create `plugins/<plugin-name>/.codex-plugin/plugin.json`. Use a stable,
   lowercase kebab-case value for `name`.
2. For a plugin that includes a skill, create
   `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`; set the manifest's
   `skills` field to `"./skills/"`.
3. Add an entry to the `plugins` array in `.agents/plugins/marketplace.json`:

   ```json
   {
     "name": "<plugin-name>",
     "source": { "source": "local", "path": "./plugins/<plugin-name>" },
     "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
     "category": "Productivity"
   }
   ```

4. Run the validation script, then manually install and test the plugin through
   `/plugins`. Do not place credentials, tokens, or other secrets in plugins,
   manifests, or the marketplace catalog.

## Reference an External Git Plugin

The marketplace can also catalog independently maintained Git plugins. When a
plugin lives in a repository subdirectory, use `git-subdir` for the entry:

```json
{
  "name": "remote-helper",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/example/codex-plugins.git",
    "path": "./plugins/remote-helper",
    "ref": "v1.2.3"
  },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
  "category": "Productivity"
}
```

For external dependencies, prefer a trusted pinned tag or commit SHA. Review the
plugin manifest, skills, MCP configuration, and hooks before publishing an entry.

## Current Contents

- **project-onboarding**: A structured skill for reading and planning changes in
  an unfamiliar codebase. It contains only a skill; it does not include MCP
  servers, hooks, connectors, or secrets.
- **photo-art-studio**: Creates photo-integrated or pure artwork from reference
  images or text briefs, with selectable visual styles and output ratios. It
  includes a purpose-built transparent logo and no MCP servers or credentials.

## Maintenance Principles

- Run `python3 scripts/validate_marketplace.py` after every marketplace or plugin
  change.
- Increment the plugin version for breaking changes and document migration steps
  in release notes.
- Review third-party hooks, MCP servers, connectors, and scripts before
  installation; these components may have read, write, or network access.
- Update only verified marketplace entries at a time. If a Git source cannot be
  resolved, Codex skips that entry without invalidating the entire marketplace.
- Treat the marketplace file and plugin manifests as the only catalog sources;
  never hand-maintain plugin cards in the website.
- Keep each local plugin directory, marketplace entry, manifest name, referenced
  asset, and website catalog record synchronized.
- Require the repository validation and website build workflow to pass before
  publishing changes to `main`.

## Official Documentation

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
