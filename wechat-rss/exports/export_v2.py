#!/usr/bin/env python3
"""Export all articles from 精彩信通 as individual HTML files - v2 with pagination."""

import json, os, re, time, urllib.request, urllib.error, datetime

BASE_URL = "http://127.0.0.1:8003/api/v1/wx"
MP_ID = "MP_WXS_3537115317"
OUTPUT_DIR = "/Users/wangrundong/work/infomation-center/wechat-rss/exports/精彩信通_html"

def login():
    url = f"{BASE_URL}/auth/login"
    data = "username=admin&password=admin%40123".encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))["data"]["access_token"]

TOKEN = login()

def api_get(path, retries=3):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
    raise last_err

def sanitize_filename(name):
    illegal = r'[\\/:*?"<>|]'
    name = re.sub(illegal, "", name)
    name = name.strip().strip(".")
    name = re.sub(r"\s+", " ", name)
    return name

def extract_body_from_full_html(full_html):
    if not full_html:
        return ""
    m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', full_html, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*(?:<script|<div)', full_html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def generate_html(article):
    title = article.get("title", "Untitled")
    mp_name = article.get("mp_name", "精彩信通")
    publish_ts = article.get("publish_time", 0)
    url = article.get("url", "")
    content_html = article.get("content_html", "") or ""

    dt = datetime.datetime.fromtimestamp(publish_ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
    date_str = dt.strftime("%Y年%m月%d日 %H:%M")

    body = content_html

    if not body or len(body) < 50:
        full_content = article.get("content", "") or ""
        if full_content and len(full_content) > 1000:
            extracted = extract_body_from_full_html(full_content)
            if extracted and len(extracted) > len(body):
                body = extracted

    if not body or len(body) < 50:
        desc = article.get("description", "") or ""
        body = f"<p>{desc}</p>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - {mp_name}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background: #f5f5f5; color: #333; line-height: 1.8; }}
  .container {{ max-width: 720px; margin: 0 auto; background: #fff; min-height: 100vh; }}
  .header {{ padding: 30px 24px 20px; border-bottom: 1px solid #eee; }}
  .header .mp-name {{ font-size: 14px; color: #576b95; margin-bottom: 8px; }}
  .header h1 {{ font-size: 22px; font-weight: 600; line-height: 1.4; margin-bottom: 12px; }}
  .header .meta {{ font-size: 13px; color: #999; }}
  .header .source-link {{ margin-top: 10px; font-size: 13px; }}
  .header .source-link a {{ color: #576b95; text-decoration: none; }}
  .content {{ padding: 20px 24px 40px; }}
  .content img {{ max-width: 100%; height: auto; display: block; margin: 10px auto; }}
  .content p {{ margin-bottom: 12px; }}
  .content section {{ margin-bottom: 12px; }}
  .footer {{ padding: 20px 24px; border-top: 1px solid #eee; font-size: 12px; color: #bbb; text-align: center; }}
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
    {body}
  </div>
  <div class="footer">
    导出自本地 wechat-rss 服务 | 精彩信通
  </div>
</div>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clear old files
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".html"):
            os.remove(os.path.join(OUTPUT_DIR, f))

    # Paginate to get all article summaries
    print("Fetching article list (paginating)...")
    all_articles = []
    offset = 0
    limit = 100
    while True:
        data = api_get(f"/articles?mp_id={MP_ID}&limit={limit}&offset={offset}")
        batch = data["data"]["list"]
        total = data["data"]["total"]
        all_articles.extend(batch)
        print(f"  Fetched {len(all_articles)}/{total}")
        if len(all_articles) >= total:
            break
        offset += limit
        time.sleep(0.2)

    print(f"Total articles to export: {len(all_articles)}")

    success = 0
    fail_list = []
    filename_count = {}
    captcha_count = 0
    short_count = 0

    for i, art_summary in enumerate(all_articles):
        art_id = art_summary["id"]
        title = art_summary.get("title", "Untitled")
        publish_ts = art_summary.get("publish_time", 0)

        dt = datetime.datetime.fromtimestamp(publish_ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
        date_prefix = dt.strftime("%Y年%m月%d日")

        try:
            detail_data = api_get(f"/articles/{art_id}")
            article = detail_data["data"]

            safe_title = sanitize_filename(title)
            base_name = f"{date_prefix}｜{safe_title}"

            # Handle duplicates
            if base_name in filename_count:
                filename_count[base_name] += 1
                file_name = f"{date_prefix}｜{safe_title}（{filename_count[base_name]}）.html"
            else:
                filename_count[base_name] = 1
                file_name = f"{base_name}.html"

            html_content = generate_html(article)
            file_path = os.path.join(OUTPUT_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Track content quality
            content_html = article.get("content_html", "") or ""
            full_content = article.get("content", "") or ""
            if "verify.js" in full_content:
                captcha_count += 1
            elif len(content_html) < 100:
                short_count += 1

            success += 1
            if (i + 1) % 20 == 0 or i == 0:
                print(f"  [{i+1}/{len(all_articles)}] {title[:45]}... -> {file_name}")

            time.sleep(0.15)

        except Exception as e:
            print(f"  [{i+1}/{len(all_articles)}] FAILED: {title[:40]}... -> {e}")
            fail_list.append({"id": art_id, "title": title, "error": str(e)})
            continue

    print(f"\n{'='*60}")
    print(f"Export complete!")
    print(f"  Directory: {OUTPUT_DIR}")
    print(f"  Total files: {len(os.listdir(OUTPUT_DIR))}")
    print(f"  Success: {success}")
    print(f"  Failed: {len(fail_list)}")
    print(f"  Captcha/verify: {captcha_count}")
    print(f"  Short content: {short_count}")
    if fail_list:
        print(f"  Failures:")
        for f in fail_list:
            print(f"    - {f['title'][:50]}: {f['error']}")


if __name__ == "__main__":
    main()
