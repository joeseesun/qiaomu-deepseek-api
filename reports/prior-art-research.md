# 先例调研 · 2026-11-13

使用乔木 Meta Skill 在 skills.sh 与 SkillsMP 各跑三组查询（DeepSeek API search fetch OCR、DeepSeek ASR TTS skill、DeepSeek document parsing）。两源均返回。按仓库和技能家族合并后 61 个候选家族。覆盖不是穷尽；没有用户评分或可比的结果质量证据。下列 GitHub Stars 是查询时的仓库关注量，与技能安装数不同。

| 检查过的原始材料 | 信号 | 取舍 |
|---|---|---|
| [qiaomu-ds-search](https://github.com/joeseesun/qiaomu-ds-search) 的 SKILL.md 和请求实现 | 6 Stars，MIT | 保留独立搜索、来源字段和禁用鉴权重定向的原则。搜索规划、跨来源去重与事实分歧仍由专用研究 skill 承担，本包保留单次处理。 |
| [DeepSeek Web Search](https://github.com/DM-Odyssey/deepseek-web-search/blob/main/oc-deepseek-search/SKILL.md) | 0 Stars；skill 声明 MIT，仓库许可未检出 | 参考区分 URL 列表和模型摘要的输出方式。采用官方当前工具类型，避免默认缓存及明文参数传密钥。未复制代码。 |
| [DeepSeek 官方 chat-demo](https://github.com/deepseek-ai/chat-demo) 的 README | 740 Stars，MIT；官方示例，非 skill | 统一 Flash Messages 与 Files，记录工具执行证据。舍弃浏览器应用、历史存储和第三方 Base URL，给一次性文档问答新增自动清理。 |
| [Agent Skills 规范](https://agentskills.io/specification) 与 [DeepSeek 官方指南](https://api-docs.deepseek.com/zh-cn/guides/build_a_chatbot/) | 官方接口和格式来源 | 单入口、按需加载参考资料；按官方 schema 区分独立工具和对话扩展。 |

设计上的新增是让 Agent 在一个入口组合网页、文件、图像及语音处理，同时保留答案、工具证据和产物路径三类信息。没有做竞品效果排名。
