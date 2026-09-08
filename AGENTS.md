# Project Rules

- Keep distributable plugins under `plugins/<plugin-name>/` and require every plugin to include `.codex-plugin/plugin.json`.
- Treat `.agents/plugins/marketplace.json` as the canonical ordered catalog. Every local plugin directory must have exactly one matching entry, and every local entry must resolve inside this repository.
- Keep plugin names synchronized across directory names, marketplace entries, and manifests.
- Every new plugin must ship with its own purpose-designed icon in the plugin
  package. Reference packaged assets from both `interface.composerIcon` and
  `interface.logo` in `.codex-plugin/plugin.json`; add `interface.logoDark` when
  a distinct dark-mode treatment is needed. Do not reuse a Skill or website
  logo as the plugin icon, and include the icon assets in every release.
- Require every marketplace category to exist in the repository-level `categories.json` allowlist.
- Preserve unrelated marketplace entries and plugin-specific metadata when maintaining one plugin.
- Keep credentials, tokens, generated build output, local runtime configuration, and installation state out of the repository.
- Generate the website catalog from repository sources. Do not hand-maintain plugin cards or duplicate catalog data in frontend code.
- Run marketplace validation, repository tests, site tests, and the production build before publication.
- Use English for repository documentation and public website copy.
