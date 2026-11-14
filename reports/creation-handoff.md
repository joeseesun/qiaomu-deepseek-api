# qiaomu-deepseek-api 1.0.0

让 Agent 用用户自己的 DeepSeek 官方 Key，执行一次性网页、文件、图像和语音任务。

- 参考了 [qiaomu-ds-search](https://github.com/joeseesun/qiaomu-ds-search) 的直接检索与来源记录、[DeepSeek Web Search](https://github.com/DM-Odyssey/deepseek-web-search/blob/main/oc-deepseek-search/SKILL.md) 的 URL 与模型摘要分离方式，以及 [官方 chat-demo](https://github.com/deepseek-ai/chat-demo) 的 Flash Messages / Files 串接。更多取舍见[先例调研](prior-art-research.md)。
- **Design advantage**：官方域名限定、密钥不放在参数和仓库、无默认结果缓存。输出同时呈现对话状态和工具结果。一次性文档问答清理自己上传的文件，附一小时有效期。
- **Validated advantage**：19 个中英文静态触发用例通过。真实 CLI 调用证据见 [output-evidence.json](output-evidence.json)；评估不代表所有模型输出正确。
- **Missing evidence**：未测内容安全拦截的覆盖率、复杂版式、真人嘈杂音频或高并发。非流式 CLI 未封装 WebSocket、连续对话历史或第三方网关。
- **回滚**：移除本包的发现路径。如曾运行 `setup`，可删除专用配置目录中的凭据文件，并在官方平台自行撤销 Key。自动清理失败时通过返回的文件 ID 清理该次上传。
