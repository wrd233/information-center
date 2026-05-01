# Mac mini 上的 RSSHub 服务

这个目录用于存放当前信息中心项目里的 RSSHub 本地部署配置。

## 为什么这样部署

- RSSHub 作为 Mac mini 上的常驻信息入口服务运行。
- Redis 用于缓存，降低重复请求和上游站点压力。
- browserless/chrome 用于支持需要浏览器渲染的 RSSHub 路由。
- 默认绑定到 `127.0.0.1:1200`，不会直接暴露到局域网或公网。

## 首次启动

```bash
cd /Users/wangrundong/work/infomation-center/rsshub
cp .env.example .env
docker compose up -d
```

打开：

```text
http://127.0.0.1:1200
```

健康检查：

```bash
curl http://127.0.0.1:1200/healthz
```

## 常用命令

```bash
docker compose ps
docker compose logs -f rsshub
docker compose restart rsshub
docker compose pull
docker compose up -d
```

## 配置写在哪里

运行配置写在当前目录的 `.env` 文件里：

```text
/Users/wangrundong/work/infomation-center/rsshub/.env
```

修改 `.env` 后，执行下面命令让配置生效：

```bash
docker compose up -d
```

常用配置：

```env
CACHE_EXPIRE=300
GITHUB_ACCESS_TOKEN=
PROXY_URI=
ALLOW_ORIGIN=*
```

部分平台路由需要额外 Cookie 或 Token。例如 B 站动态路由常见配置：

```env
BILIBILI_COOKIE_你的B站UID=SESSDATA=...; bili_jct=...; DedeUserID=...
```

如果订阅的是 B 站 UP 主投稿视频路由 `/bilibili/user/video/:uid/:disableEmbed?`，服务端还可能需要在 `.env` 中配置 `BILIBILI_DM_IMG_LIST`。这个值属于部署环境配置，不要写死在脚本或 OPML 里。

如果不确定某个路由需要什么配置，优先查看 RSSHub 官方文档里的对应路由和部署配置说明。

## B 站 UP 主投稿订阅

当前 B 站 UP 主订阅只关注“投稿视频”，不使用“用户动态”路由。

RSSHub 路由：

```text
/bilibili/user/video/:uid/:disableEmbed?
```

示例：

```text
http://127.0.0.1:1200/bilibili/user/video/2267573
```

规则：

- `uid` 使用 UP 主主页里的数字 ID，例如 `https://space.bilibili.com/2267573`。
- `disableEmbed` 可选；不填时 RSS 内容会嵌入视频。
- 关闭内嵌视频时使用 `/bilibili/user/video/2267573/1`。
- `BILIBILI_COOKIE_{uid}` 主要用于 B 站动态、关注列表等需要登录态的路由。
- `BILIBILI_DM_IMG_LIST` 是 RSSHub 服务端环境变量，可能用于 B 站 UP 主投稿系列路由，应写在 `.env`，不要写进脚本或 OPML。

修改 `.env` 后必须重建 RSSHub 容器，否则运行中的容器不会拿到新环境变量：

```bash
cd /Users/wangrundong/work/infomation-center/rsshub
docker compose up -d rsshub
```

检查容器是否拿到 B 站配置：

```bash
docker compose exec -T rsshub /bin/sh -lc 'env | grep -E "^BILIBILI"'
```

本机验证示例：

```bash
curl -I http://127.0.0.1:1200/bilibili/user/video/1366786686
```

如果返回 `412 Precondition Failed`、`风控校验失败` 或 RSSHub `503`，优先检查 `.env` 中的 B 站变量是否已进入容器。

## OPML 迁移

原始 OPML：

```text
/Users/wangrundong/work/infomation-center/rsshub/myrss.opml
```

已迁移成本机 RSSHub 地址的 OPML：

```text
/Users/wangrundong/work/infomation-center/rsshub/myrss.local.opml
```

迁移逻辑是把下面这些公共或第三方 RSSHub 实例：

```text
https://rsshub.app/...
https://rssgod.zeabur.app/...
```

替换为：

```text
http://127.0.0.1:1200/...
```

普通博客、微信公众号第三方服务、X/Twitter 第三方服务、anyfeeder 等非 RSSHub 源不会被替换。

## 局域网或远程访问

建议继续让 RSSHub 绑定在 `127.0.0.1`，再通过下面任一方式对外提供访问：

- Tailscale：适合只给自己的设备私密访问。
- Caddy 或 Nginx + Basic Auth：适合局域网或受控公网访问。
- Cloudflare Tunnel 或 Cloudflare Access：适合不开放路由器端口的远程访问。

如果确实希望 RSSHub 直接暴露到局域网，可以修改 `.env`：

```env
RSSHUB_BIND=0.0.0.0
```

不建议把 RSSHub 直接裸露到公网。

当前远程访问建议使用 Tailscale Serve，具体见：

```text
/Users/wangrundong/work/infomation-center/rsshub/TAILSCALE.md
```

## Apple Silicon 注意事项

默认镜像通常可以在 Docker Desktop 或 OrbStack 上运行。如果 `browserless/chrome` 在 Mac mini 上遇到镜像或运行问题，可以改用 RSSHub 自带 Chromium 的镜像，并移除 `browserless` 依赖：

```env
RSSHUB_IMAGE=diygod/rsshub:chromium-bundled
```

同时需要从 `docker-compose.yml` 中移除 `PUPPETEER_WS_ENDPOINT`、`browserless` 服务，以及 RSSHub 对 `browserless` 的依赖。
