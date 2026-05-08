# AI Intelligence

AI 情报编辑器 —— 自动采集、筛选、总结并发布 AI 行业动态，用大白话为中文读者解读真正重要的 AI 新闻。

## 核心流程

```
信息采集 → 自动筛选 → AI 总结 → 人话翻译 → 影响分析 → 自动发布
```

每天海量的 AI 新闻中，只有约 5% 值得关注。本项目通过 AI 自动完成信息筛选和内容提炼，让你高效获取 AI 行业的关键变化。

## 项目结构

```
sources/          数据采集 —— 每个数据源独立目录
  official/       官方源（OpenAI、Anthropic、Google AI、HuggingFace、GitHub）
  community/      社区源（Reddit、HackerNews、Twitter 等）
pipelines/        数据处理流水线（采集、清洗、总结、分类、发布）
ai/               AI 处理层 —— 与业务代码隔离
  llm/            LLM 客户端 + 路由（通过 LiteLLM 统一调用）
  prompts/        Prompt 模板
  tasks/          AI 任务：总结、解读、标签、评分、趋势分析
storage/          原始数据存储（始终保留原文，支持更换模型/Prompt 后重跑）
  raw/ cleaned/ summarized/ published/
configs/          配置中心（settings.py、sources.yaml）
database/         SQLite 数据模型
scripts/          脚本入口（run_daily.py 等）
services/         业务逻辑
publishing/       发布适配器（Telegram、微信公众号、邮件、Markdown）
tests/            单元测试
doc/              产品文档
```

## 数据流

```
Crawler → Raw JSON → Clean Pipeline → AI Summarize → Daily Digest → Telegram
```

## 技术栈

- **语言**: Python
- **Web 框架**: FastAPI
- **任务调度**: APScheduler
- **数据库**: SQLite
- **爬虫**: feedparser、requests、BeautifulSoup4、Playwright
- **LLM 调用**: LiteLLM（统一接口调用 OpenAI、Claude、Gemini）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 API Key 等配置
```

### 3. 运行每日任务

```bash
python scripts/run_daily.py
```

## 内容筛选规则

**值得报道：**
- AI 能力的实质性变化（更强推理、更长上下文、更低成本）
- 对行业有实际影响（岗位替代、降低创业成本、改变开发方式）
- 社区爆火信号（GitHub Star 暴涨、Reddit 热议、Twitter 传播）

**不值得报道：**
- 融资新闻
- 小幅 benchmark 提升
- 营销软文

## 内容模板

每条情报按统一结构输出：

1. **发生了什么** —— 一句话概括
2. **人话解释** —— 普通人能看懂的解读
3. **会影响谁** —— 受影响的群体
4. **未来趋势** —— 值得关注的方向

## 设计原则

- 数据源只负责采集，流水线只负责处理，AI 层只负责调用 LLM —— 职责严格分离
- 原始数据始终保留在 `storage/raw/`，支持随时更换 Prompt 或模型重跑
- 所有 LLM 调用统一通过 `ai/llm/router.py`，业务代码不直接调用任何模型 API
- 数据源配置集中在 `configs/sources.yaml`

## License

MIT
