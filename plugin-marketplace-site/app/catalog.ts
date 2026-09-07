export type PluginRecord = {
  name: string;
  displayName: string;
  summary: string;
  longDescription: string;
  version: string;
  developerName: string;
  category: string;
  capabilities: string[];
  logoUrl: string | null;
  sourceUrl: string;
};

export type CatalogSnapshot = {
  schemaVersion: number;
  generatedAt: string;
  marketplace: { name: string; displayName: string };
  repository: { name: string; url: string; branch: string; commit: string };
  plugins: PluginRecord[];
};

export function filterPlugins(
  plugins: PluginRecord[],
  query: string,
  category: string,
): PluginRecord[] {
  const needle = query.trim().toLowerCase();
  return plugins.filter((plugin) => {
    const searchable = [
      plugin.name,
      plugin.displayName,
      plugin.summary,
      plugin.longDescription,
      plugin.developerName,
      plugin.category,
      ...plugin.capabilities,
    ]
      .join(" ")
      .toLowerCase();
    return (
      (category === "All" || plugin.category === category) &&
      (!needle || searchable.includes(needle))
    );
  });
}
