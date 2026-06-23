import { Database, List, Settings, Upload } from "lucide-react";
import type { Page } from "../App";

interface Props {
  page: Page;
  onPageChange: (page: Page) => void;
  children: React.ReactNode;
}

export function Layout({ page, onPageChange, children }: Props) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <Database size={22} aria-hidden="true" />
          <div>
            <h1>RSS Source Manager</h1>
            <span>127.0.0.1</span>
          </div>
        </div>
        <nav className="tabs" aria-label="Primary">
          <button className={page === "sources" ? "active" : ""} onClick={() => onPageChange("sources")}>
            <List size={17} aria-hidden="true" />源列表
          </button>
          <button className={page === "import-export" ? "active" : ""} onClick={() => onPageChange("import-export")}>
            <Upload size={17} aria-hidden="true" />导入导出
          </button>
          <button className={page === "settings" ? "active" : ""} onClick={() => onPageChange("settings")}>
            <Settings size={17} aria-hidden="true" />设置
          </button>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}

