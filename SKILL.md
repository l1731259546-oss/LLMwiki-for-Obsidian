---
name: "LLMwiki-for-Obsidian"
description: "能使用ObsidianCLI直接操控Obsidian客户端和获取Obsidian客户端的状态。管理基于 Karpathy 思路的 LLM Wiki 个人知识库系统。支持创建仓库结构、摄入来源、lint 检查、知识合成。Invoke 当需要搭建或维护 Obsidian LLM Wiki 知识库时。"
---
# 必要环境依赖
**开始任务前必须确认是否已安装以下必要环境依赖**
- Node.js
- qmd（npm install -g @tobi/qmd）

# LLMwiki for Obsidian

这是一个基于 Andrej Karpathy 的 LLM Wiki 思路的个人知识库管理技能，帮助你在 Obsidian 中搭建和维护三层架构的知识系统。

## 架构设计


### 设计原则
| 原则 | 含义 |
| :--- | :--- |
| LLM 是编译器，不是检索器 | 知识被「编译」一次后持久存在，而非每次查询重新推导 |
| Raw 层不可变 | 原始来源绝对不会被 LLM 修改，永远是你的真实记录 |
| Raw 层完整性由 SHA-256 守护 | 每次摄入记录哈希，lint 时检测文件是否被篡改 |
| 输出必须持久化 | 每次有价值的答案都写入 wiki/outputs/，不会消失在对话历史中 |
| 矛盾必须显式标注 | 来源之间的分歧会被明确记录，不会静默覆盖 |
| 认知演化可追踪 | 每个 concept 页的 Evolution Log 记录了认知如何随来源积累而演变 |
| 个人立场独立存储 | 自己写的文章不参与 confidence 计数，立场标注为「第一手认知」 |
| confidence: high 必须用户确认 | 不能自动晋升，必须用户明确背书 |


### 核心三层架构

| 层级 | 归属者 | 内容 | 规则 |
| :--- | :--- | :--- | :--- |
| **Raw 原始层** | 人类 | 剪裁文章、PDF、图片、笔记 | **IMMUTABLE**，LLM 绝不修改，只读 |
| **Wiki 编译层** | LLM 完全拥有 | Markdown 实体/概念/来源/合成页 | 全部由 LLM 写入，人类只读浏览 |
| **Outputs 层** | LLM 生成 | Q&A 答案、图表、Marp 幻灯片 | 输出必须回写入 Wiki，不消失于对话历史 |

## 目录结构

```
wikiknowledge-base/
├── raw/                        # 人类所有，LLM 只读
│   ├── articles/               # 手动保存的文章（Markdown）
│   ├── clippings/              # Obsidian Web Clipper 剪藏（主要入口）
│   ├── images/                 # 截图和图片
│   ├── pdfs/                   # PDF 文件及配套元数据文件
│   ├── notes/                  # 随手记录
│   └── personal/               # 自己写的文章、分析报告、投资笔记
├── wiki/                       # LLM 完全自助管理
│   ├── index.md                # 面向内容的索引（graph-excluded）
│   ├── log.md                  # 仅追加的操作日志（graph-excluded）
│   ├── overview.md             # 高层综述 + Health Dashboard（graph-excluded）
│   ├── QUESTIONS.md            # 开放问题队列（graph-excluded）
│   ├── sources/                # 每个来源的摘要页
│   ├── concepts/               # 思想、模式、技术
│   ├── entities/               # 人物、工具、机构、论文
│   ├── synthesis/              # 跨来源合成分析
│   └── templates/              # 页面模板（LLM 使用）
├── outputs/                    # 查询答案、图表、幻灯片、lint 报告
├── scripts/
│   └── lint_check.py           # Wiki 健康检查脚本（9 项检查）
│   └── qmd-reindex.sh          # qmd 索引重建脚本
├── Agent.md                    # LLM 行为契约（核心文件）
└── README.md                   # 项目说明
```

## Frontmatter 规范
页面需要YAML头部规范，以下是示例：
```
---
type: source-summary
title: "{{title}}"
date: YYYY-MM-DD
source_url: "{{url}}"
domain: "{{domain}}"
author: "{{author}}"
tags: [wiki, wiki/source]
processed: true
raw_file: "raw/articles/filename.md"
raw_sha256: "<64-char-hex>"
last_verified: YYYY-MM-DD
---
```

## 可用操作

### 1. create-vault
创建全新的 LLM Wiki 仓库目录结构和所有系统文件。请参见 `/references/create-vault.md`

### 2. ingest
将 raw/ 目录中的新原始来源摄入到 wiki 中，提取概念和实体，更新已有页面。请参见 `/references/ingest.md`

### 3. query
回答用户问题，基于 wiki 中已有的知识合成答案，写入 outputs。请参见 `/references/query.md`

### 4. reflect
四阶段反思合成：反向检验 → 模式扫描 → 深度合成 → 缺口分析。请参见 `/references/reflect.md`

### 5. lint
运行完整的 9 项健康检查，生成 lint 报告。请参见 `/references/lint.md`

### 6. lint_check
执行 9 项具体检查的 Python 脚本。请参见 `/references/lint_check.md`

### 7. merge
合并重复概念/实体页面，处理跨语言合并。请参见 `/references/merge.md`

### 8. add-question
添加开放问题到队列。请参见 `/references/add-question.md`

## 核心规则

### **Wikilink 使用规范（铁律，不可违反）**
- 所有 wikilink 目标必须使用**英文小写连字符**格式
- ✅ `[[value-investing]]` ✅ `[[attention-mechanism]]` ✅ `[[warren-buffett]]`
- ❌ `[[价值投资]]`（中文词汇）❌ `[[ValueInvesting]]`（驼峰）❌ `[[value_investing]]`（下划线）
### **Wiki 语言规范**
- Wiki 层（concept/entity/synthesis 页）统一用**中文写作**
- concept 页 `title` 字段使用**中文主名称**（用于图谱节点显示）
- 英文术语首次出现时括号标注：`注意力机制（Attention Mechanism）`
- 所有 slug（文件名）统一用英文小写连字符，不使用中文文件名
- `aliases` 字段覆盖中英文所有叫法
### **Confidence 更新规则**
| 来源数量 | Confidence | 处理方式 |
| --- | --- | --- |
| 1 个来源 | low | 自动设置 |
| 3+ 个来源 | medium | 自动设置 |
| 5+ 个来源且无重大矛盾 | 候选 high | 向用户展示 Definition 和 Sources 列表，等待确认 |
| 用户明确回复「确认」或「ok」 | high | 才可设置 |
> 注意：个人写作（raw/personal/）不参与 source_count 计数
### **Source Integrity Rules**
- re-ingest 规则：若 lint 报告 ⚠ SOURCE MODIFIED，需重新摄入该文件并更新所有受影响的 concept/entity 页面，Evolution Log 记录「YYYY-MM-DD 来源更新：[[slug]] 哈希变更，内容已重新提取」
- 来源超过 2 年标注 possibly_outdated: true
- 矛盾来源必须在 source 页和 concept 页的 Contradictions 节显式记录，不得静默覆盖
### **系统文件隔离规则**
以下文件的 frontmatter 必须含 `graph-excluded: true`，不参与 Obsidian 图谱：
- `wiki/log.md`
- `wiki/index.md`
- `wiki/overview.md`
- `wiki/QUESTIONS.md`
- `wiki/outputs/` 下所有文件
### **文档维护规则**
当 CLAUDE.md 规则更新时，同步更新 USER_GUIDE.md 对应章节，确保两份文档一致。

## 调用时机
- 需要从零搭建 LLM Wiki 知识库仓库时 → `create-vault`
- 需要将新的文章/PDF/笔记摄入到知识库时 → `ingest`
- 需要基于知识库回答问题时 → `query`
- 需要对知识库进行健康检查时 → `lint`
- 需要合并重复概念时 → `merge`
- 需要添加开放问题时 → `add-question`
- 需要进行跨来源知识合成反思时 → `reflect`

## 用能直接控制 Obsidian客户端的skills，可以关注Obsidian客户端的状态确保操作成功
`/obsidian-bases`
`/obsidian-cli`
`/obsidian-defuddle`
`/obsobsidian-json-canvas`