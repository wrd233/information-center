#!/usr/bin/env node

const fs = require('fs');

const [, , input, output, baseUrl] = process.argv;

if (!input || !output || !baseUrl) {
  console.error('用法：node scripts/rewrite-opml-base.js 输入.opml 输出.opml 新RSSHub地址');
  console.error('示例：node scripts/rewrite-opml-base.js myrss.local.opml myrss.tailscale.opml https://macmini-rsshub.example.ts.net');
  process.exit(1);
}

const normalizedBase = baseUrl.replace(/\/+$/, '');
let content = fs.readFileSync(input, 'utf8');
let count = 0;

content = content.replace(/xmlUrl="http:\/\/127\.0\.0\.1:1200([^"]*)"/g, (_, path) => {
  count += 1;
  return `xmlUrl="${normalizedBase}${path}"`;
});

fs.writeFileSync(output, content);
console.log(`已生成：${output}`);
console.log(`已替换本机 RSSHub 地址：${count} 个`);
