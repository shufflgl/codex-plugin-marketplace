# Plugin Marketplace Site

This static website is the public catalog for `shufflgl/codex-plugin-marketplace`. Its plugin cards, metadata, categories, versions, capabilities, source links, and logos are generated from `.agents/plugins/marketplace.json` and each plugin manifest during every build.

## Local development

Requires Bun and Node.js 22.13 or newer.

```sh
bun install
bun run dev
```

## Validation

```sh
bun run lint
bun run test
bun run build:pages
```

The static deployment output is written to `out/` and is excluded from source control.
