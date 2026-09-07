import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { filterPlugins } from "../app/catalog.ts";

const plugins = [
  { name: "design-tool", displayName: "Design Tool", summary: "Create images.", longDescription: "Create visual assets.", version: "1.0.0", developerName: "Maker", category: "Design", capabilities: ["Image generation"], logoUrl: null, sourceUrl: "https://example.com" },
  { name: "planning-tool", displayName: "Planning Tool", summary: "Plan projects.", longDescription: "Structure project work.", version: "1.0.0", developerName: "Maker", category: "Productivity", capabilities: [], logoUrl: null, sourceUrl: "https://example.com" },
];

test("searches plugin metadata and filters categories", () => {
  assert.deepEqual(filterPlugins(plugins, "visual", "All").map((item) => item.name), ["design-tool"]);
  assert.deepEqual(filterPlugins(plugins, "", "Productivity").map((item) => item.name), ["planning-tool"]);
});

test("generated catalog is public and includes every plugin", async () => {
  const raw = await readFile(new URL("../.generated/catalog.json", import.meta.url), "utf8");
  assert.doesNotMatch(raw, /\/(?:Users|home|private|Volumes)\//);
  const catalog = JSON.parse(raw);
  assert.ok(catalog.plugins.length >= 1);
  assert.ok(catalog.plugins.every((plugin) => plugin.sourceUrl.startsWith("https://")));
});
