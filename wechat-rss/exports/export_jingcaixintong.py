#!/usr/bin/env python3
"""Export all articles from 精彩信通 as individual HTML files."""

import json
import os
import re
import time
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8003/api/v1/wx"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MDE5NjAzMn0.AczNzTHdyr0APK4N5V28UQonjOPcA85FvqIR9pKxRZs"
MP_ID = "MP_WXS_3537115317"
OUTPUT_DIR = "/Users/wangrundong/work/infomation-center/wechat-rss/exports/精彩信通_html"


def api_get(path, retries=3):
    """Call the wechat-rss API with retries."""
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, json.JSONDecodeError, ConnectionResetError) as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise last_err


def sanitize_filename(name):
    """Remove illegal filename characters."""
    # Replace illegal chars with full-width alternatives or remove
    illegal = r'[\\/:*?"<>|]'
    name = re.sub(illegal, "", name)
    # Remove leading/trailing whitespace and dots
    name = name.strip().strip(".")
    # Collapse multiple spaces
    name = re.sub(r"\s+", " ", name)
    return name


def clean_content_html(html):
    """Remove noise sections from article body."""
    if not html:
        return ""

    # Patterns to remove (non-body content)
    noise_patterns = [
        # WeChat reader interaction prompts
        r'<p[^>]*>\s*预览时标签不可点\s*</p>',
        r'<p[^>]*>\s*微信扫一扫[^<]*</p>',
        r'<p[^>]*>\s*关注该公众号\s*</p>',
        # Common tail sections
        r'<section[^>]*>.*?往期推荐.*?</section>',
        r'<section[^>]*>.*?阅读原文.*?</section>',
        # Continue reading / read more prompts
        r'<p[^>]*>\s*(继续阅读|阅读全文|展开全文)\s*</p>',
        # "Read original article" links at bottom
        r'<p[^>]*>\s*<a[^>]*>\s*阅读原文\s*</a>\s*</p>',
        # Share/like/view interaction sections at bottom
        r'<section[^>]*>.*?(分享|收藏|点赞|在看).*?</section>',
    ]

    for pattern in noise_patterns:
        html = re.sub(pattern, "", html, flags=re.DOTALL | re.IGNORECASE)

    # Try to cut content at "往期推荐" or similar section headers
    cut_markers = [
        r'<section[^>]*>.*?往期推荐.*?</section>',
        r'<p[^>]*>.*?<strong[^>]*>往期推荐</strong[^>]*>.*?</p>',
        r'<p[^>]*>.*?<span[^>]*>往期推荐</span[^>]*>.*?</p>',
    ]

    for marker in cut_markers:
        m = re.search(marker, html, re.DOTALL | re.IGNORECASE)
        if m:
            html = html[: m.start()]
            break

    return html.strip()


def generate_html(article):
    """Generate a complete HTML page for an article."""
    title = article.get("title", "Untitled")
    mp_name = article.get("mp_name", "精彩信通")
    publish_ts = article.get("publish_time", 0)
    url = article.get("url", "")
    content_html = article.get("content_html", "") or ""

    # Convert timestamp to readable format
    import datetime
    dt = datetime.datetime.fromtimestamp(publish_ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
    date_str = dt.strftime("%Y年%m月%d日 %H:%M")

    # Clean content
    body_html = clean_content_html(content_html)

    # If no content_html, try description
    if not body_html:
        desc = article.get("description", "") or ""
        body_html = f"<p>{desc}</p>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - {mp_name}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: #f5f5f5;
    color: #333;
    line-height: 1.8;
  }}
  .container {{
    max-width: 720px;
    margin: 0 auto;
    background: #fff;
    min-height: 100vh;
  }}
  .header {{
    padding: 30px 24px 20px;
    border-bottom: 1px solid #eee;
  }}
  .header .mp-name {{
    font-size: 14px;
    color: #576b95;
    margin-bottom: 8px;
  }}
  .header h1 {{
    font-size: 22px;
    font-weight: 600;
    line-height: 1.4;
    margin-bottom: 12px;
  }}
  .header .meta {{
    font-size: 13px;
    color: #999;
  }}
  .header .source-link {{
    margin-top: 10px;
    font-size: 13px;
  }}
  .header .source-link a {{
    color: #576b95;
    text-decoration: none;
  }}
  .content {{
    padding: 20px 24px 40px;
  }}
  .content img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 10px auto;
  }}
  .content p {{
    margin-bottom: 12px;
  }}
  .content section {{
    margin-bottom: 12px;
  }}
  .footer {{
    padding: 20px 24px;
    border-top: 1px solid #eee;
    font-size: 12px;
    color: #bbb;
    text-align: center;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="mp-name">{mp_name}</div>
    <h1>{title}</h1>
    <div class="meta">发布时间：{date_str}</div>
    <div class="source-link">原文链接：<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a></div>
  </div>
  <div class="content">
    {body_html}
  </div>
  <div class="footer">
    导出自本地 wechat-rss 服务 | 精彩信通
  </div>
</div>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching article list...")
    # Fetch all articles in one request (29 total, limit 50 is safe)
    list_data = api_get(f"/articles?mp_id={MP_ID}&limit=50&offset=0")
    articles = list_data["data"]["list"]
    total = list_data["data"]["total"]
    print(f"Total articles available: {total}, fetched: {len(articles)}")

    success_count = 0
    fail_list = []
    filename_count = {}

    for i, art_summary in enumerate(articles):
        art_id = art_summary["id"]
        title = art_summary.get("title", "Untitled")
        publish_ts = art_summary.get("publish_time", 0)

        import datetime
        dt = datetime.datetime.fromtimestamp(publish_ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
        date_prefix = dt.strftime("%Y年%m月%d日")

        print(f"[{i+1}/{len(articles)}] Fetching detail: {title}")

        try:
            detail_data = api_get(f"/articles/{art_id}")
            article = detail_data["data"]

            # Generate filename
            safe_title = sanitize_filename(title)
            base_name = f"{date_prefix}｜{safe_title}"

            # Handle duplicates
            if base_name in filename_count:
                filename_count[base_name] += 1
                file_name = f"{date_prefix}｜{safe_title}（{filename_count[base_name]}）.html"
            else:
                filename_count[base_name] = 1
                file_name = f"{base_name}.html"

            # Generate HTML
            html_content = generate_html(article)

            # Write file
            file_path = os.path.join(OUTPUT_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            success_count += 1
            print(f"  -> Saved: {file_name}")

            # Small delay between requests
            time.sleep(0.3)

        except Exception as e:
            print(f"  -> FAILED: {e}")
            fail_list.append({"id": art_id, "title": title, "error": str(e)})
            continue

    print(f"\n{'='*60}")
    print(f"Export complete!")
    print(f"  Directory: {OUTPUT_DIR}")
    print(f"  Success: {success_count}")
    print(f"  Failed: {len(fail_list)}")
    if fail_list:
        print(f"  Failures:")
        for f in fail_list:
            print(f"    - {f['title']}: {f['error']}")


if __name__ == "__main__":
    main()
