from __future__ import annotations

from collections import OrderedDict
from datetime import datetime, timezone
import xml.etree.ElementTree as ET


def parse_opml(text: str) -> list[dict[str, str]]:
    root = ET.fromstring(text)
    body = root.find("body")
    if body is None:
        return []
    items: list[dict[str, str]] = []

    def walk(node: ET.Element, path: list[str]) -> None:
        for child in list(node):
            xml_url = child.attrib.get("xmlUrl") or child.attrib.get("xmlurl")
            title = child.attrib.get("title") or child.attrib.get("text") or xml_url or ""
            if xml_url:
                items.append(
                    {
                        "display_name": title,
                        "feed_url": xml_url,
                        "original_feed_url": xml_url,
                        "category": "/".join(path) if path else "未分类",
                        "html_url": child.attrib.get("htmlUrl") or child.attrib.get("htmlurl") or "",
                        "type": child.attrib.get("type") or "rss",
                    }
                )
            else:
                label = child.attrib.get("text") or child.attrib.get("title")
                walk(child, [*path, label] if label else path)

    walk(body, [])
    return items


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


def build_opml(sources: list[dict[str, str]], title: str = "RSS Source Manager") -> str:
    opml = ET.Element("opml", {"version": "2.0"})
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = title
    ET.SubElement(head, "dateCreated").text = datetime.now(timezone.utc).isoformat(timespec="seconds")
    body = ET.SubElement(opml, "body")
    cache: dict[tuple[int, str], ET.Element] = OrderedDict()
    for source in sources:
        parent = ensure_path(body, cache, source.get("category", "未分类"))
        attrs = {
            "text": source["display_name"],
            "title": source["display_name"],
            "type": "rss",
            "xmlUrl": source["feed_url"],
        }
        if source.get("html_url"):
            attrs["htmlUrl"] = source["html_url"]
        ET.SubElement(parent, "outline", attrs)
    ET.indent(opml, space="    ")
    return ET.tostring(opml, encoding="unicode", xml_declaration=True)

