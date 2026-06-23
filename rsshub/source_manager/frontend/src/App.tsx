import { useState } from "react";
import { Layout } from "./components/Layout";
import { SourceListPage } from "./pages/SourceListPage";
import { ImportExportPage } from "./pages/ImportExportPage";
import { SettingsPage } from "./pages/SettingsPage";

export type Page = "sources" | "import-export" | "settings";

export default function App() {
  const [page, setPage] = useState<Page>("sources");
  return (
    <Layout page={page} onPageChange={setPage}>
      {page === "sources" && <SourceListPage />}
      {page === "import-export" && <ImportExportPage />}
      {page === "settings" && <SettingsPage />}
    </Layout>
  );
}

