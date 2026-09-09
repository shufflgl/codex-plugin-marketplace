import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server renders the repository-backed plugin catalog", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /Codex Plugin Marketplace/);
  assert.match(html, /src="\/marketplace-logo\.png"/);
  assert.match(html, /href="\/favicon\.ico"/);
  assert.doesNotMatch(html, /\/_next\/image/);
  assert.match(html, /Search plugins/);
  assert.match(html, /Install/);
  assert.match(html, /shufflgl\/codex-plugin-marketplace/);
  assert.doesNotMatch(html, /SKILL Agora|Download Bilibili Audio/);
});
