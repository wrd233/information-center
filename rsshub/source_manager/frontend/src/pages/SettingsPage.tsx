import { ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { SettingsPayload } from "../api/types";

export function SettingsPage() {
  const [settings, setSettings] = useState<SettingsPayload | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    api.settings().then(setSettings).catch((error) => setMessage(error.message));
  }, []);

  if (message) return <div className="notice">{message}</div>;
  if (!settings) return <div className="notice">loading</div>;

  return (
    <div className="page-stack">
      <section className="panel">
        <h2>设置</h2>
        <dl>
          <dt>database_path</dt><dd>{settings.database_path}</dd>
          <dt>config_path</dt><dd>{settings.config_path}</dd>
          <dt>server</dt><dd>{JSON.stringify(settings.server)}</dd>
          <dt>health</dt><dd>{JSON.stringify(settings.health)}</dd>
          <dt>fetch</dt><dd>{JSON.stringify(settings.fetch)}</dd>
          <dt>batch_fetch</dt><dd>{JSON.stringify(settings.batch_fetch)}</dd>
          <dt>docs</dt><dd><a href={settings.docs_url}><ExternalLink size={15} aria-hidden="true" />/docs</a></dd>
        </dl>
      </section>
      <section className="detail-grid">
        <div className="panel"><h3>adapters</h3><pre>{JSON.stringify(settings.adapters, null, 2)}</pre></div>
        <div className="panel"><h3>export profiles</h3><pre>{JSON.stringify(settings.export_profiles, null, 2)}</pre></div>
      </section>
    </div>
  );
}

