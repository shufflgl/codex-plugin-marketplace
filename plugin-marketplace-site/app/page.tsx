"use client";

import { useMemo, useState } from "react";
import { Check, Copy, ExternalLink, PackagePlus, X } from "lucide-react";
import { FaGithub } from "react-icons/fa6";
import Image from "next/image";
import Link from "next/link";
import snapshotData from "../.generated/catalog.json";
import { filterPlugins, type CatalogSnapshot, type PluginRecord } from "./catalog";

const snapshot = snapshotData as CatalogSnapshot;

export default function Home() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const [selected, setSelected] = useState<PluginRecord | null>(null);
  const [copied, setCopied] = useState(false);
  const categories = useMemo(
    () => ["All", ...Array.from(new Set(snapshot.plugins.map((item) => item.category))).sort()],
    [],
  );
  const visible = useMemo(
    () => filterPlugins(snapshot.plugins, query, category),
    [category, query],
  );

  const installCommand = selected
    ? `codex plugin marketplace add shufflgl/codex-plugin-marketplace\ncodex plugin add ${selected.name}@${snapshot.marketplace.name}`
    : "";

  async function copyInstallCommand() {
    if (!selected) return;
    await navigator.clipboard.writeText(installCommand);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <main>
      <header className="site-header">
        <Link className="brand" href="/" aria-label="Codex Plugin Marketplace home">
          <Image src="/marketplace-logo.png" alt="" width={38} height={38} priority />
          <span>Plugin Marketplace</span>
        </Link>
        <a className="github-link" href={snapshot.repository.url} target="_blank" rel="noreferrer" aria-label="Open GitHub repository">
          <FaGithub size={19} aria-hidden="true" />
        </a>
      </header>

      <section className="hero" aria-labelledby="page-title">
        <p className="eyebrow">CODEX PLUGIN CATALOG</p>
        <h1 id="page-title">Install one capability.<br />Keep the workflow focused.</h1>
        <p>Repository-maintained plugins with inspectable manifests, source, and installation paths.</p>
      </section>

      <section className="catalog" aria-labelledby="catalog-title">
        <div className="catalog-tools">
          <label className="search">
            <span className="sr-only">Search plugins</span>
            <input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search plugins" />
          </label>
          <div className="categories" aria-label="Plugin categories">
            {categories.map((item) => (
              <button key={item} type="button" className={category === item ? "active" : ""} onClick={() => setCategory(item)} aria-pressed={category === item}>
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="catalog-heading">
          <h2 id="catalog-title">{category === "All" ? "All plugins" : category}</h2>
          <span>{visible.length}</span>
        </div>

        <div className="plugin-grid">
          {visible.map((plugin) => (
            <article className="plugin-card" key={plugin.name}>
              <div className="card-topline">
                {plugin.logoUrl ? <Image className="plugin-logo" src={plugin.logoUrl} alt="" width={64} height={64} /> : <div className="plugin-logo fallback" aria-hidden="true" />}
                <div className="card-meta"><span>{plugin.category}</span><span>v{plugin.version}</span></div>
              </div>
              <h3>{plugin.displayName}</h3>
              <p>{plugin.summary}</p>
              <div className="capabilities">
                {plugin.capabilities.slice(0, 3).map((item) => <span key={item}>{item}</span>)}
              </div>
              <div className="card-actions">
                <button type="button" onClick={() => { setCopied(false); setSelected(plugin); }}>
                  <PackagePlus size={16} aria-hidden="true" /> Install
                </button>
                <a href={plugin.sourceUrl} target="_blank" rel="noreferrer">Source <ExternalLink size={14} aria-hidden="true" /></a>
              </div>
            </article>
          ))}
        </div>

        {visible.length === 0 && <div className="empty"><strong>No matching plugins.</strong><span>Try another search or category.</span></div>}
      </section>

      <footer><span>{snapshot.plugins.length} maintained plugins</span><span>{snapshot.repository.name}</span></footer>

      {selected && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setSelected(null); }}>
          <section className="install-modal" role="dialog" aria-modal="true" aria-labelledby="install-title">
            <div className="modal-header">
              <div><p className="eyebrow">INSTALL PLUGIN</p><h2 id="install-title">{selected.displayName}</h2></div>
              <button className="close-button" type="button" aria-label="Close" onClick={() => setSelected(null)}><X size={18} /></button>
            </div>
            <p className="modal-intro">Add the marketplace once, then install this plugin. Start a new Codex session after installation.</p>
            <pre><code>{installCommand}</code></pre>
            <button className="copy-button" type="button" onClick={copyInstallCommand}>
              {copied ? <Check size={16} /> : <Copy size={16} />}{copied ? "Copied" : "Copy commands"}
            </button>
          </section>
        </div>
      )}
    </main>
  );
}
