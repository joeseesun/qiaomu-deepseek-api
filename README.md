# qiaomu-deepseek-api

一份扫描 PDF、一段录音和一个网页，原本得分别接三个工具。装好这个 Skill 后，可以让 Agent 用你的 DeepSeek API Key 读文档、转写、查网页和生成配音，并拿到可核对的结果。

[![Stars](https://img.shields.io/github/stars/joeseesun/qiaomu-deepseek-api)](https://github.com/joeseesun/qiaomu-deepseek-api/stargazers)
[![Forks](https://img.shields.io/github/forks/joeseesun/qiaomu-deepseek-api)](https://github.com/joeseesun/qiaomu-deepseek-api/forks)
[![Issues](https://img.shields.io/github/issues/joeseesun/qiaomu-deepseek-api)](https://github.com/joeseesun/qiaomu-deepseek-api/issues)
[![Last commit](https://img.shields.io/github/last-commit/joeseesun/qiaomu-deepseek-api)](https://github.com/joeseesun/qiaomu-deepseek-api/commits/main/)
[![MIT](https://img.shields.io/github/license/joeseesun/qiaomu-deepseek-api)](LICENSE)

[中文](#安装) · [English](#english)

> 问扫描件「只返回验证编号」→ `CEDAR-63842`，同时返回 `cleanup.deleted: true`。这是随附 CLI 的真接口测试结果。

## 安装

```bash
npx skills add joeseesun/qiaomu-deepseek-api
```

- [ ] 使用支持 Agent Skills 的工具，安装命令需要 Node.js/npm。
- [ ] 运行命令需要 Python 3.10 或更新版本，无需安装 Python 包。
- [ ] 在 [DeepSeek 开放平台](https://platform.deepseek.com/api_keys) 获取自己的 API Key，通过宿主的密钥配置注入 `DEEPSEEK_API_KEY`。也可以在自己的终端进入 Skill 目录运行 `python3 scripts/deepseek_api.py setup`，隐藏输入并验证后保存到本机专用配置文件。首次执行发现未配置时，Agent 会给出官方申请入口和配置命令，再继续原任务。不要将 Key 发到聊天。

TTS 会在你没指定音色时提供单选卡，在不支持卡片的宿主里用文字选项。两款音色使用同一句话实测，可下载试听：[海星 Stella 女声](assets/voices/stella.mp3) · [暗潮 Tide 男声](assets/voices/tide.mp3)。

## 用法

你可以直接这样说：

- “用 DeepSeek 审一下这个扫描 PDF，告诉我汇款金额和票号。”
- “用 DeepSeek 查官方发布，给我引用和可打开的链接。”
- “用 DeepSeek 以图搜图，查这张公开图片的出处。”
- “用 DeepSeek 把这段 WAV 转文字，再用 Stella 给我的新稿生成配音。”

| 要拿到什么 | 选什么 |
|---|---|
| 搜索结果、网页 Markdown | 独立 Search / Fetch，无需对话模型 |
| 带引用的答案、深度搜索、读链接、以图搜图 | Flash 对话工具 |
| 文档里的内容、表格或插图 | 上传后问答，完成后清理本次上传 |
| 图片/扫描件的逐页文字 | 独立 OCR |
| 音频转写、普通话 WAV 配音 | ASR / TTS，可组合 |

也可以直接跑脚本：

```bash
python3 scripts/deepseek_api.py search 'DeepSeek API site:api-docs.deepseek.com' --count 3
python3 scripts/deepseek_api.py ask-file report.pdf --prompt '列出三项关键数字'
python3 scripts/deepseek_api.py tts --text '你好，欢迎收听。' --voice stella --output demo.wav
```

[完整命令与输出约定](references/commands.md) · [验证与限制](reports/creation-handoff.md)

## 常见问题 · Troubleshooting

| 现象 | 怎么处理 |
|---|---|
| 401 或 `missing_key` | 检查宿主注入的官方 Key；环境变量优先于本机配置。 |
| 402 / 429 | 分别检查账户余额、等待限流缓解。CLI 不会自动重试。 |
| MP3 不能转写 | 先转为 16 位 PCM WAV 或 Ogg Opus，单段最长 120 秒。 |
| 回答有文字但缺来源 | 检查 `tool_calls` / `tool_results`，需要网页正文时直接用 Fetch。 |
| 模型读不懂 PDF 插图 | 使用 `rich_layout_recognition` 或把插图单独作为图片输入，核对颜色、数字和标注。 |

上传或输入的内容会发送给 DeepSeek；工具用量可能收费。本机输入与密钥不会被打包到 Skill。卸载可从 Agent 的技能目录移除本包；如曾运行 `setup`，可自行删除专用凭据文件并在平台撤销 Key。

本地验证用 `python3 -m unittest discover -s tests`。也可用 [乔木 Meta Skill](https://github.com/joeseesun/qiaomu-meta-skill) 的 `validate_skill.py` 检查包格式。

<!-- qiaomu-profile:start -->
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

## English

Use your own DeepSeek API key with one Python CLI for web search, Markdown fetch, file Q&A, OCR, transcription, and speech synthesis. Flash chat can also search deeply, read links, and reverse-search an image. Requests go to the official DeepSeek endpoint.

Install using the command above. Set `DEEPSEEK_API_KEY` in your agent host, or run `python3 scripts/deepseek_api.py setup` in your own terminal. Try “Use DeepSeek to summarize this PDF and list the key amounts” or “Use DeepSeek TTS to save this narration as WAV.” The [command reference](references/commands.md) includes the parameters and output fields. Python 3.10+ and network access are required. Tool usage can be billable, and submitted content is sent to DeepSeek.
