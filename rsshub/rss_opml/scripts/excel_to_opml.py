#!/usr/bin/env python3
"""Convert rss_sources.xlsx into an OPML 2.0 file.

Default layout:
  The workbook contains four source sheets: Articles, SocialMedia, Pictures, Videos.
  Each sheet name becomes the OPML top-level category.
  The category_path column only stores custom subcategories inside that sheet.

Usage:
  python3 scripts/excel_to_opml.py rss_sources.xlsx exports/myrss.generated.opml --title "My RSS"
  python3 scripts/excel_to_opml.py rss_sources.xlsx exports/articles.opml --sheets Articles --title "Articles"

Rows with enabled not in Y/YES/TRUE/1/启用/是 are skipped.
This script uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

DEFAULT_SHEETS = ["Articles", "SocialMedia", "Pictures", "Videos"]
TRUE_VALUES = {"y", "yes", "true", "1", "启用", "是", "active"}
NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def normalize_header(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    return text.replace(" ", "_").replace("-", "_")


def pick(row: dict[str, Any], *names: str, default: str = "") -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return default


def is_enabled(value: Any, export_all: bool = False) -> bool:
    if export_all:
        return True
    if value is None:
        return False
    return str(value).strip().lower() in TRUE_VALUES


def parse_sheets(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def col_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref.upper())
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - ord("A") + 1
    return value - 1


def read_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    values = []
    for si in root.findall(f"{NS_MAIN}si"):
        parts = [node.text or "" for node in si.findall(f".//{NS_MAIN}t")]
        values.append("".join(parts))
    return values


def sheet_paths(zf: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {}
    for rel in rels.findall(f"{NS_PKG_REL}Relationship"):
        target = rel.attrib.get("Target", "")
        if target.startswith("/"):
            path = target.lstrip("/")
        else:
            path = "xl/" + target.lstrip("/")
        rel_map[rel.attrib.get("Id", "")] = path
    result = {}
    for sheet in workbook.findall(f".//{NS_MAIN}sheet"):
        name = sheet.attrib.get("name", "")
        rel_id = sheet.attrib.get(f"{NS_REL}id", "")
        if name and rel_id in rel_map:
            result[name] = rel_map[rel_id]
    return result


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{NS_MAIN}t"))
    value_node = cell.find(f"{NS_MAIN}v")
    if value_node is None or value_node.text is None:
        return ""
    raw = value_node.text
    if cell_type == "s":
        try:
            return shared_strings[int(raw)]
        except (ValueError, IndexError):
            return raw
    if cell_type == "b":
        return "TRUE" if raw == "1" else "FALSE"
    return raw


def read_sheet(zf: zipfile.ZipFile, path: str, shared_strings: list[str]) -> list[list[str]]:
    root = ET.fromstring(zf.read(path))
    rows = []
    for row in root.findall(f".//{NS_MAIN}sheetData/{NS_MAIN}row"):
        values: list[str] = []
        for cell in row.findall(f"{NS_MAIN}c"):
            idx = col_index(cell.attrib.get("r", ""))
            while len(values) <= idx:
                values.append("")
            values[idx] = cell_text(cell, shared_strings).strip()
        while values and values[-1] == "":
            values.pop()
        rows.append(values)
    return rows


def join_category(sheet_name: str, category_path: str) -> str:
    parts = [sheet_name.strip()]
    parts.extend(part.strip() for part in category_path.split("/") if part and part.strip())
    return "/".join(part for part in parts if part)


def read_sheet_rows(rows: list[list[str]], sheet_name: str, export_all: bool, seen_xml_urls: set[str]) -> list[dict[str, str]]:
    if not rows:
        return []
    headers = [normalize_header(value) for value in rows[0]]
    result = []
    for idx, values in enumerate(rows[1:], start=2):
        if not any(str(value).strip() for value in values):
            continue
        row = dict(zip(headers, values))
        if not is_enabled(pick(row, "enabled"), export_all=export_all):
            continue
        xml_url = pick(row, "xml_url", "xmlurl", "feed_url", "rss_url")
        if not xml_url:
            print(f"[skip] {sheet_name}!{idx}: missing xml_url", file=sys.stderr)
            continue
        if xml_url in seen_xml_urls:
            print(f"[skip] {sheet_name}!{idx}: duplicate xml_url: {xml_url}", file=sys.stderr)
            continue
        seen_xml_urls.add(xml_url)
        subcategory = pick(row, "category_path", "category", "folder")
        result.append({
            "category_path": join_category(sheet_name, subcategory),
            "title": pick(row, "title", "text", default=xml_url),
            "xml_url": xml_url,
            "html_url": pick(row, "html_url", "htmlurl", "site_url", "homepage"),
            "type": pick(row, "type", default="rss"),
        })
    return result


def read_sources(xlsx_path: Path, sheets: list[str], export_all: bool) -> list[dict[str, str]]:
    with zipfile.ZipFile(xlsx_path) as zf:
        shared_strings = read_shared_strings(zf)
        paths = sheet_paths(zf)
        if sheets == DEFAULT_SHEETS and not any(name in paths for name in DEFAULT_SHEETS) and "Sources" in paths:
            sheets = ["Sources"]
        missing = [name for name in sheets if name not in paths]
        if missing:
            raise SystemExit(f"Sheet not found: {', '.join(missing)}. Available: {', '.join(paths)}")
        seen_xml_urls: set[str] = set()
        result = []
        for sheet_name in sheets:
            result.extend(read_sheet_rows(read_sheet(zf, paths[sheet_name], shared_strings), sheet_name, export_all, seen_xml_urls))
        return result


def ensure_path(parent: ET.Element, cache: dict[tuple[int, str], ET.Element], category_path: str) -> ET.Element:
    current = parent
    for raw_part in category_path.split("/"):
        part = raw_part.strip()
        if not part:
            continue
        key = (id(current), part)
        if key not in cache:
            cache[key] = ET.SubElement(current, "outline", {"text": part})
        current = cache[key]
    return current


def build_opml(sources: list[dict[str, str]], title: str) -> ET.ElementTree:
    opml = ET.Element("opml", {"version": "2.0"})
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = title
    ET.SubElement(head, "dateCreated").text = datetime.now(timezone.utc).isoformat(timespec="seconds")
    body = ET.SubElement(opml, "body")
    category_cache: dict[tuple[int, str], ET.Element] = OrderedDict()
    for item in sources:
        parent = ensure_path(body, category_cache, item["category_path"])
        attrs = {
            "text": item["title"],
            "title": item["title"],
            "xmlUrl": item["xml_url"],
            "type": item["type"] or "rss",
        }
        if item.get("html_url"):
            attrs["htmlUrl"] = item["html_url"]
        ET.SubElement(parent, "outline", attrs)
    ET.indent(opml, space="    ")
    return ET.ElementTree(opml)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert RSS source Excel to OPML.")
    parser.add_argument("xlsx", type=Path, help="Path to rss_sources.xlsx")
    parser.add_argument("opml", type=Path, help="Output OPML path")
    parser.add_argument("--sheets", default=",".join(DEFAULT_SHEETS), help="Comma-separated sheet names to export, default: Articles,SocialMedia,Pictures,Videos")
    parser.add_argument("--title", default="My RSS", help="OPML title")
    parser.add_argument("--all", action="store_true", help="Export all rows with xml_url, ignoring enabled")
    args = parser.parse_args()
    sheets = parse_sheets(args.sheets)
    sources = read_sources(args.xlsx, sheets, export_all=args.all)
    if not sources:
        raise SystemExit("No sources to export. Check enabled column and xml_url values.")
    args.opml.parent.mkdir(parents=True, exist_ok=True)
    build_opml(sources, args.title).write(args.opml, encoding="utf-8", xml_declaration=True)
    print(f"Exported {len(sources)} RSS sources from {', '.join(sheets)} to {args.opml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
