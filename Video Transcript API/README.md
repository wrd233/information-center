# Video Transcript API

当前原型先实现 B 站和小红书入口，按“平台适配器只负责获取材料”的边界封装 BBDown 与 XHS-Downloader。

## 能力边界

B 站适配器输出：

- 字幕文件
- 音频文件
- 封面
- 标题和分 P 信息（基于 BBDown 输出尽力解析）
- 下载状态
- 从字幕整理出的原始正文

它暂时不做：

- 深度摘要
- 知识库归档
- 项目素材库分发

无字幕时会下载音频，并把任务状态置为 `needs_asr`，留给下一层 ASR worker 接手。
B 站任务默认会额外保存音频文件；如果只想保留平台字幕，可在请求里设置 `"download_audio": false`。

小红书适配器输出：

- XHS-Downloader 返回的作品元数据
- 视频下载地址
- 视频文件（可选，默认下载）
- 从视频提取的音频文件（可选，默认提取）
- 标题、文案、作者、作品 ID

小红书视频笔记当前没有走平台字幕能力，拿到音频后任务状态会置为 `needs_asr`。

## 粗筛 ASR 设计

粗筛阶段的目标不是产出可发布字幕，而是用较小的 CPU 和时间成本，尽快得到足够判断内容价值的纯文本。它默认牺牲一部分完整性和精度，换取更快的筛选速度。

设计原则：

- 平台适配器只负责拿材料；ASR worker 负责音频预处理和转写。
- 所有来源的音频先统一成 `16kHz / mono / wav`，减少后端 ASR 的格式差异。
- 先用 VAD 去掉静音，再决定是否抽样。这样抽样窗口按“有效语音时长”计算，而不是按原始视频时长计算。
- 短音频完整粗转，长音频只取代表性片段。粗筛先判断“值不值得看”，不追求全量记录。
- 预处理产物保存在任务目录，方便复查同一段音频被喂给 ASR 的实际内容。

预处理流水线：

```text
原始音频
-> ffmpeg 提取/转码
-> 16kHz 单声道 WAV
-> Silero VAD 去静音
-> 按语音时长选择全量或抽样
-> asr_preprocess/rough_asr_input.wav
-> ASR backend
-> transcript.txt
```

抽样规则：

- 小于等于 5 分钟：VAD 去静音后全量粗转。
- 大于 5 分钟：VAD 去静音后抽取前 2 分钟 + 中间 2 分钟 + 结尾 1 分钟。
- 如果 VAD 没识别出语音，会回退到 `16kHz / mono / wav` 的标准化音频，避免误删整段内容。
- 抽样后的最终输入文件固定为 `asr_preprocess/rough_asr_input.wav`。

VAD 选择：

- 默认使用 Silero VAD。
- Silero VAD 的模型很小，适合粗筛前处理；JIT/ONNX CPU 推理都适合在低占用场景下运行。
- 项目默认使用 ONNX 路线：`ASR_VAD_ONNX=1`。

这套 trick 对不同 ASR 后端都是通用收益：CapsWriter、FunASR/Paraformer、sherpa-onnx 或后续其他本地 ASR，都可以直接吃同一个 `rough_asr_input.wav`。

中间产物：

```text
asr_preprocess/normalized_16k_mono.wav
asr_preprocess/vad_speech_16k_mono.wav
asr_preprocess/rough_asr_input.wav
asr_preprocess/preprocess_result.json
```

单独验证预处理：

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
PYTHONPATH=. python3 -m app.audio_preprocess "<audio-path>" --workspace "<task-dir>" --json
```

临时跳过 VAD，只验证转码和抽样：

```bash
ASR_VAD_ENABLED=0 \
PYTHONPATH=. python3 -m app.audio_preprocess "<audio-path>" --workspace "<task-dir>" --json
```

## ASR 后端：FunASR / Paraformer

当前推荐走 FunASR runtime 的 CPU 离线文件转写服务，而不是直接把 CapsWriter 桌面端接进 API。
原因是 CapsWriter 的主线定位是本机语音输入工具；它背后的 Paraformer/Sherpa-ONNX 思路适合低延迟桌面输入，但服务化、Docker 化、长音频文件转写这块 FunASR runtime 更直接。

这个项目里的 ASR worker 只做粗筛转录：

- 输入：任务结果里的 `audio` artifact
- 预处理：统一 16k 单声道 WAV，Silero VAD 去静音，再按长度选择全量或抽样
- 输出：任务工作目录下的 `transcript.txt`
- 不输出时间轴
- 默认连接 `ws://127.0.0.1:10095`
- 通过 Docker 的 `cpus`、FunASR 的 `decoder-thread-num` / `io-thread-num` / `model-thread-num` 限制 CPU 占用

可调环境变量：

```text
ASR_PREPROCESS_ENABLED=1
ASR_SAMPLE_RATE=16000
ASR_VAD_ENABLED=1
ASR_VAD_ONNX=1
ASR_VAD_THRESHOLD=0.5
ASR_VAD_MIN_SPEECH_MS=250
ASR_VAD_MIN_SILENCE_MS=100
ASR_VAD_SPEECH_PAD_MS=120
ASR_FULL_DURATION_SECONDS=300
ASR_LONG_HEAD_SECONDS=120
ASR_LONG_MIDDLE_SECONDS=120
ASR_LONG_TAIL_SECONDS=60
```

如果想让粗筛更激进，可以把 `ASR_VAD_THRESHOLD` 提到 `0.6`；如果担心漏掉轻声、背景声里的讲话，可以降到 `0.35` 到 `0.45`，并把 `ASR_VAD_SPEECH_PAD_MS` 提到 `200`。

安装 Python client 依赖：

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
python3 -m pip install -r requirements.txt
```

`silero-vad` 会带上 `torch` / `torchaudio` 依赖；它的模型很小，但 Python 运行时依赖不算小。如果只想临时跳过 VAD，可设置 `ASR_VAD_ENABLED=0`。

启动 CPU 版 Paraformer 服务：

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
docker compose -f docker-compose.asr.yml up -d
```

当前默认镜像是：

```text
registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-cpu-0.4.1
```

如果要换成其他标签：

```bash
FUNASR_IMAGE=registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-cpu-0.4.7 \
docker compose -f docker-compose.asr.yml up -d
```

默认 CPU 策略偏保守：

```text
FUNASR_CPUS=2.0
FUNASR_DECODER_THREAD_NUM=1
FUNASR_IO_THREAD_NUM=1
FUNASR_MODEL_THREAD_NUM=1
```

如果想再快一点，可以逐步增加：

```bash
FUNASR_CPUS=4 \
FUNASR_DECODER_THREAD_NUM=2 \
FUNASR_IO_THREAD_NUM=1 \
FUNASR_MODEL_THREAD_NUM=1 \
docker compose -f docker-compose.asr.yml up -d
```

对单个 `needs_asr` 任务触发转录：

```bash
curl -X POST http://127.0.0.1:8765/api/jobs/<job_id>/asr
```

也可以跑独立 worker，持续消费 `needs_asr` 任务：

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
PYTHONPATH=. FUNASR_WS_URL=ws://127.0.0.1:10095 python3 -m app.asr_worker
```

只跑一轮：

```bash
PYTHONPATH=. FUNASR_WS_URL=ws://127.0.0.1:10095 python3 -m app.asr_worker --once --limit 1
```

## 安装 BBDown

BBDown 不随本项目打包。官方 README 推荐两种方式：

```bash
dotnet tool install --global BBDown
```

或从 GitHub Release 下载二进制文件：

https://github.com/nilaoda/BBDown/releases

本机还需要 `ffmpeg`，当前机器已检测到 `/opt/homebrew/bin/ffmpeg`。

## 启动

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
PYTHONPATH=. \
BBDOWN_BIN="$PWD/tools/bbdown/BBDown" \
FFMPEG_PATH=/opt/homebrew/bin/ffmpeg \
python3 -m app.server
```

默认监听：

```text
http://127.0.0.1:8765
```

如果 BBDown 二进制不叫 `BBDown`，可以设置：

```bash
BBDOWN_BIN=/path/to/BBDown PYTHONPATH=. python3 -m app.server
```

本项目当前已在 `tools/bbdown/BBDown` 放置了 macOS arm64 版 BBDown。其他系统请替换成对应平台的二进制。

需要 cookie 时：

```bash
BBDOWN_COOKIE='SESSDATA=...' PYTHONPATH=. python3 -m app.server
```

## 启动 XHS-Downloader

小红书适配器依赖外部 XHS-Downloader API 服务。可用源码或 Docker 启动：

```bash
python main.py api
```

默认服务地址为：

```text
http://127.0.0.1:5556
```

本服务会调用 XHS-Downloader 的 `POST /xhs/detail`，只请求作品详情和下载地址，然后由本项目下载视频并用 `ffmpeg` 提取音频。可通过环境变量配置：

```bash
XHS_API_BASE_URL=http://127.0.0.1:5556 \
XHS_COOKIE='a1=...' \
XHS_PROXY='http://127.0.0.1:10808' \
FFMPEG_PATH=/opt/homebrew/bin/ffmpeg \
PYTHONPATH=. python3 -m app.server
```

## API

健康检查：

```bash
curl http://127.0.0.1:8765/health
```

创建 B 站任务：

```bash
curl -X POST http://127.0.0.1:8765/api/bilibili/jobs \
  -H 'content-type: application/json' \
  -d '{
    "url": "https://www.bilibili.com/video/BV1xx411c7mD",
    "select_page": "ALL",
    "download_audio": true,
    "download_audio_if_no_subtitle": true,
    "project": "demo",
    "note": "first bilibili adapter test"
}'
```

创建小红书任务：

```bash
curl -X POST http://127.0.0.1:8765/api/xhs/jobs \
  -H 'content-type: application/json' \
  -d '{
    "url": "https://www.xiaohongshu.com/explore/作品ID?xsec_token=XXX",
    "download_video": true,
    "extract_audio": true,
    "skip_existing_download_record": false,
    "project": "demo",
    "note": "first xhs adapter test"
  }'
```

`/api/xiaohongshu/jobs` 是同一个入口的长名称别名。支持 `xhslink.com` 分享短链；如遇功能异常，建议为 XHS-Downloader 配置最新 Cookie。

查看任务：

```bash
curl http://127.0.0.1:8765/api/jobs/<job_id>
```

列出任务：

```bash
curl http://127.0.0.1:8765/api/jobs
```

## 本地测试

```bash
cd "/Users/wangrundong/work/infomation-center/Video Transcript API"
PYTHONPATH=. python3 -m unittest discover -s tests
```
