# 通过 Tailscale 远程访问 RSSHub

本文档说明如何让另一台不在同一局域网内的电脑访问 Mac mini 上的 RSSHub。

## 当前方案

RSSHub 继续只监听 Mac mini 本机：

```env
RSSHUB_BIND=127.0.0.1
RSSHUB_PORT=1200
```

这样 RSSHub 不会直接暴露给家里局域网或公网。远程访问通过 Tailscale Serve 完成：

```text
另一台电脑 -> Tailscale 私有网络 -> Mac mini Tailscale Serve -> http://127.0.0.1:1200
```

## Mac mini 端

当前使用 Homebrew 安装的 Tailscale CLI：

```bash
brew install tailscale
```

由于普通 Homebrew 服务默认需要 root 创建系统网卡，本机改用 userspace-networking 模式运行，启动项在：

```text
/Users/wangrundong/Library/LaunchAgents/com.local.tailscale-userspace.plist
```

Tailscale CLI 需要指定 socket：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock status
```

也可以使用本目录里的简化脚本：

```bash
cd /Users/wangrundong/work/infomation-center/rsshub
./scripts/tailscale.sh status
```

首次登录：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock up --hostname=macmini-rsshub
```

当前 Mac mini 的 Tailscale 信息：

```text
主机名：macmini-rsshub
Tailscale IP：100.124.134.33
Serve 地址：https://macmini-rsshub.tail99ecfa.ts.net/
```

登录完成后，发布 RSSHub：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock serve --bg http://127.0.0.1:1200
```

查看发布状态：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock serve status
```

查看 Tailscale IP：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock ip -4
```

## 另一台电脑

1. 安装 Tailscale：<https://tailscale.com/download>
2. 登录和 Mac mini 同一个 Tailscale 账号。
3. 在 Tailscale 管理后台确认能看到 `macmini-rsshub`。
4. 使用 Mac mini 的 Tailscale Serve 地址访问 RSSHub：

```text
https://macmini-rsshub.tail99ecfa.ts.net/
```

健康检查地址：

```text
https://macmini-rsshub.tail99ecfa.ts.net/healthz
```

如果另一台 Mac 开了系统代理、Privoxy、Clash、Surge 等代理工具，需要把 Tailscale 地址加入代理绕过列表。否则浏览器可能把 `*.ts.net` 请求交给代理，出现 `500 Internal Privoxy Error`、`ERR_CONNECTION_CLOSED` 等错误。

建议加入代理绕过列表：

```text
*.ts.net,macmini-rsshub.tail99ecfa.ts.net,macmini-rsshub,100.64.0.0/10,100.124.134.33
```

也可以在另一台 Mac 终端里绕过代理验证：

```bash
curl --noproxy '*' https://macmini-rsshub.tail99ecfa.ts.net/healthz
curl --noproxy '*' http://macmini-rsshub.tail99ecfa.ts.net:1200/healthz
```

如果没有使用 Serve，也可以在 Mac mini 端把 RSSHub 绑定到 Tailscale IP 后访问 `http://Tailscale-IP:1200`，但不推荐作为首选方案。

## OPML 地址转换

本机使用的 OPML：

```text
/Users/wangrundong/work/infomation-center/rsshub/myrss.local.opml
```

它里面的 RSSHub 地址是：

```text
http://127.0.0.1:1200
```

另一台电脑不能使用这个地址。拿到 Tailscale Serve 地址后，用脚本生成远程版 OPML：

```bash
cd /Users/wangrundong/work/infomation-center/rsshub
node scripts/rewrite-opml-base.js myrss.local.opml myrss.tailscale.opml https://macmini-rsshub.tail99ecfa.ts.net
```

然后在另一台电脑的 RSS 阅读器里导入：

```text
/Users/wangrundong/work/infomation-center/rsshub/myrss.tailscale.opml
```

当前远程版 OPML 已生成，RSSHub 类订阅地址已经替换为：

```text
https://macmini-rsshub.tail99ecfa.ts.net
```

## 常见排查

确认 RSSHub 本机可用：

```bash
curl http://127.0.0.1:1200/healthz
```

确认 Tailscale 登录状态：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock status
```

确认 Serve 配置：

```bash
tailscale --socket=/Users/wangrundong/.local/share/tailscale/tailscaled.sock serve status
```

如果另一台电脑打不开，优先检查：

- 两台机器是否登录同一个 Tailscale 账号。
- Mac mini 是否在线。
- RSSHub 是否健康。
- OPML 里是否还保留 `127.0.0.1:1200`。
- 另一台电脑的代理是否绕过了 `*.ts.net` 和 `100.64.0.0/10`。

注意：Mac mini 当前使用 userspace-networking 模式，本机浏览器不一定能解析 `macmini-rsshub.tail99ecfa.ts.net` 这个 MagicDNS 地址；另一台正常安装 Tailscale 客户端的电脑通常可以直接解析和访问。
