# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供项目指导。

## 项目概述

AI Intelligence —— 一个"AI 情报编辑器"，面向中文读者，自动采集、筛选、总结并发布 AI 行业动态。

核心流水线：**采集 → 筛选 → AI 总结 → 人话翻译 → 影响分析 → 自动发布**

产品文档：`doc/产品落地.md`、`doc/目录结构.md`

## 目录结构

```
sources/          数据采集 —— 每个数据源独立目录
  official/       官方源（OpenAI、Anthropic、Google AI、HuggingFace、GitHub）
  community/      社区源（Reddit、HackerNews、Twitter 等）
pipelines/        数据处理流水线（采集、清洗、总结、分类、发布）
ai/               AI 处理层 —— 与业务代码隔离
  llm/            LLM 客户端 + 路由（通过 LiteLLM 统一接口）
  prompts/        Prompt 模板
  tasks/          AI 任务：总结、解读、标签、评分、趋势分析
storage/          原始数据存储（始终保留原文，切勿丢弃）
  raw/ cleaned/ summarized/ published/
configs/          配置中心（settings.py、sources.yaml）
database/         SQLite 数据模型与迁移
scripts/          脚本入口（run_daily.py、rebuild_summary.py 等）
services/         业务逻辑（文章、排行、趋势、日报）
publishing/       发布适配器（Telegram、微信公众号、邮件、Markdown）
```

核心职责分离：**数据源只负责采集**，**流水线只负责处理**，**AI 层只负责调用 LLM**。严禁混用职责。

## 技术栈

- Python、FastAPI、APScheduler、SQLite
- 爬虫：`feedparser`、`requests`、`beautifulsoup4`、`playwright`
- LLM 调用：LiteLLM 统一接口（OpenAI、Claude、Gemini）
- 安装依赖：`pip install -r requirements.txt`

## 数据流

```
爬虫 → 原始 JSON → 清洗流水线 → AI 总结 → 每日日报 → Telegram
```

## 内容筛选规则

- 每天约 5% 的 AI 新闻值得报道
- 值得报道：AI 能力变化、行业实际影响、社区爆火信号
- 不值得报道：融资新闻、小幅 benchmark 提升、营销软文
- 内容模板：(1) 发生了什么、(2) 人话解释、(3) 会影响谁、(4) 未来趋势
- 标题必须用大白话，禁止使用技术黑话

## 设计约束

- MVP 阶段不做用户系统、登录、评论、社交功能
- 原始文章数据必须始终保留在 `storage/raw/`（更换 Prompt/模型后需要重跑）
- 所有 LLM 调用统一通过 `ai/llm/router.py` —— 业务代码禁止直接调用 OpenAI/Claude
- 数据源配置集中在 `configs/sources.yaml`
