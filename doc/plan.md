Plan: OpenAI 单源全流程打通                                                                                                                                                                                               
                                                                                                                                                                                                                           
 Context

 OpenAI RSS 爬虫已完成（Collect），需要打通后续管道：Clean → AI Summarize → Publish (Telegram)，实现单源端到端验证。

 实现步骤

 1. AI 层（基础设施）

 - configs/settings.py — 添加 LLM_MODEL, LLM_TEMPERATURE
 - ai/llm/router.py — LiteLLM 封装，一个 ask(prompt, system, model, temperature) 函数
 - ai/prompts/score.py — 评分 prompt（1-10，判断是否值得报道）
 - ai/prompts/summarize.py — 摘要 prompt（人话标题、发生了什么、人话解释、影响人群、未来趋势）
 - ai/prompts/impact.py — 影响分析 prompt（具体角色、趋势）
 - ai/tasks/score.py — score_article(article) -> int
 - ai/tasks/summarize.py — summarize_article(article) -> dict
 - ai/tasks/analyze.py — analyze_impact(article, summary) -> dict

 2. Clean Pipeline

 - pipelines/clean_pipeline.py — load_raw → deduplicate → score_and_filter → 保存到 storage/cleaned/

 3. Summarize Pipeline

 - pipelines/summarize_pipeline.py — 加载 cleaned → AI 摘要 + 影响分析 → 保存到 storage/summarized/

 4. Telegram 发布

 - publishing/telegram.py — format_digest 格式化 + send_telegram 发送（requests POST）

 5. 编排脚本

 - scripts/run_daily.py — Collect → Clean → Summarize → Publish 串联

 6. 测试

 - 所有 LLM 调用 mock，所有 HTTP 请求 mock，不依赖网络

 关键文件

 - 修改: configs/settings.py, .env.example
 - 新建: ai/llm/router.py, ai/prompts/*.py, ai/tasks/*.py
 - 新建: pipelines/clean_pipeline.py, pipelines/summarize_pipeline.py
 - 新建: publishing/telegram.py
 - 新建: scripts/run_daily.py

 验证方式

 - python -m pytest tests/ -v 全部通过
 - python scripts/run_daily.py 端到端运行（需配置 API key 和 Telegram token）