# LLMwiki-for-Obsidian

[![Obsidian](https://img.shields.io/badge/Obsidian-Plugin-purple?logo=obsidian)](https://obsidian.md/) [![Trae Skill](https://img.shields.io/badge/Trae-Skill-blue)](https://trae.ai)

一个基于 Andrej Karpathy 的 LLM Wiki 思路的个人知识库管理技能，帮助你在 Obsidian 中搭建和维护 **三层架构**（Raw / Wiki / Outputs）的知识系统。

## 使用简述（小白不清楚怎么用agent skill的，详细的流程在下面）
建议先安装obsidian客户端，和带读取写入工具的agent(基本都带,比如codex和claude code这些)。
这样你的agent在装上skill以后，你仅仅需要手动做两步就可以完成资料摄入wiki知识库，并可以在obsidian直观看见你的wiki树状图动态的一点一线的长出来。
    1. 手动把资料拖进指定文件夹
    2. 跟agent说创建wiki结构并摄入刚手动拖进去的文件
        - 提示词里指令显性调用skill就更加有约束力度
        - 愿意折腾的还可以在装些obsidianCLI的skill，如果你装了的话你的agent可以直接通过CLI交互obsidian客户端

## ✨ 特性

- 🏗️ **三层架构**：Raw（人类所有，只读）→ Wiki（LLM 编译层）→ Outputs（LLM 输出）
- 🔒 **SHA-256 完整性守护**：原始文件哈希校验，检测篡改
- 🌐 **跨语言支持**：中英文术语自动对齐，aliases 别名匹配
- 🔍 **qmd 索引加速**：基于 qmd 的快速语义检索
- 🛡️ **Wikilink 规范检查**：9 项自动化健康检查
- 📝 **认知演化追踪**：每个 concept 页的 Evolution Log
- 🤖 **深度 Obsidian 集成**：通过 Obsidian CLI 操控客户端

## 📋 环境依赖

开始之前，确保已安装以下必要环境：

| 依赖 | 版本要求 | 安装命令 |
|------|---------|----------|
| [Node.js](https://nodejs.org/) | >= 18 | 官网下载或 `nvm install 20` |
| [qmd](https://github.com/tobi/qmd) | 最新 | `npm install -g @tobi/qmd` |
| [Obsidian](https://obsidian.md/) | 最新 | 官网下载 |

验证安装：
```bash
node --version     # 应 >= 18
qmd --version      # 应显示版本号
```

## 🚀 安装方法

### 方法一：通过 Trae Skill 安装（推荐）

1. 打开 Trae，进入你的 Obsidian 仓库所在的工作区
2. 在 Skill 面板中搜索 `LLMwiki-for-Obsidian`
3. 点击安装即可

### 方法二：手动安装

1. 克隆本仓库到 Trae 的 skills 目录：

```bash
# Windows
cd %USERPROFILE%\.trae-cn\skills
git clone https://github.com/l1731259546-oss/LLMwiki-for-Obsidian.git

# macOS / Linux
cd ~/.trae/skills
git clone https://github.com/l1731259546-oss/LLMwiki-for-Obsidian.git
```

2. 安装 Python 依赖（用于 lint 检查脚本）：

```bash
pip install PyYAML
```

3. 重启 Trae 客户端，Skill 即可自动加载

### 方法三：直接使用

如果你不想安装为 Skill，也可以直接使用本仓库的功能：

```bash
# 克隆仓库
git clone https://github.com/l1731259546-oss/LLMwiki-for-Obsidian.git

# 运行 lint 检查
python scripts/lint_check.py /path/to/your/knowledge-base
```

## 📖 使用方法

本 Skill 提供以下 8 个核心操作：

### 1. `create-vault` — 创建知识库

从零创建完整的 LLM Wiki 仓库目录结构和所有系统文件。

```
触发时机：首次搭建知识库时
```

### 2. `ingest` — 摄入来源

将 raw/ 目录中的新原始来源（文章、PDF、笔记）摄入到 wiki 中，提取概念和实体，更新已有页面。

```
触发时机：有新的文章/PDF/笔记需要入库时
```

### 3. `query` — 基于知识库回答问题

基于 wiki 中已有的知识合成答案，写入 outputs。

```
触发时机：需要基于已有知识库回答问题时
```

### 4. `reflect` — 知识合成反思

四阶段反思合成：反向检验 → 模式扫描 → 深度合成 → 缺口分析。

```
触发时机：定期（每月）进行知识库反思、摄入足够多新材料后
```

### 5. `lint` — 健康检查

运行完整的 9 项健康检查，生成 lint 报告。

```
触发时机：定期维护、批量摄入后、用户要求检查时
```

### 6. `lint_check` — Python 检查脚本

执行 9 项具体检查的 Python 脚本，可独立运行。

```bash
python scripts/lint_check.py /path/to/knowledge-base
```

### 7. `merge` — 合并重复概念

合并重复的概念或实体页面，处理同语言和跨语言合并。

```
触发时机：lint 报告发现近重复概念、用户发现重复概念时
```

### 8. `add-question` — 添加开放问题

将开放问题添加到 QUESTIONS.md 队列，供后续研究回答。

```
触发时机：摄入过程中发现新的研究问题、用户提出暂无法回答的问题时
```

## 🏛️ 架构设计

### 核心三层架构

| 层级 | 归属者 | 内容 | 规则 |
|:---|:---|:---|:---|
| **Raw 原始层** | 人类 | 剪裁文章、PDF、图片、笔记 | **IMMUTABLE**，LLM 绝不修改 |
| **Wiki 编译层** | LLM 拥有 | 实体/概念/来源/合成页 | 全部由 LLM 写入 |
| **Outputs 层** | LLM 生成 | Q&A 答案、图表、幻灯片 | 输出必须回写入 Wiki |

### 设计原则

- **LLM 是编译器，不是检索器**：知识被「编译」一次后持久存在
- **Raw 层不可变**：原始来源绝对不会被 LLM 修改
- **Raw 层完整性由 SHA-256 守护**：每次摄入记录哈希
- **输出必须持久化**：每次有价值的答案都写入 wiki/outputs/
- **矛盾必须显式标注**：来源之间的分歧会被明确记录
- **认知演化可追踪**：每个 concept 页的 Evolution Log
- **个人立场独立存储**：自己写的文章不参与 confidence 计数
- **confidence: high 必须用户确认**：不能自动晋升

### 目录结构

```
wikiknowledge-base/
├── raw/                        # 人类所有，LLM 只读
│   ├── articles/               # 手动保存的文章
│   ├── clippings/              # Obsidian Web Clipper 剪藏
│   ├── images/                 # 截图和图片
│   ├── pdfs/                   # PDF 文件
│   ├── notes/                  # 随手记录
│   └── personal/               # 自己写的文章
├── wiki/                       # LLM 完全自助管理
│   ├── index.md                # 内容索引（graph-excluded）
│   ├── log.md                  # 操作日志（graph-excluded）
│   ├── overview.md             # 健康仪表盘（graph-excluded）
│   ├── QUESTIONS.md            # 开放问题队列（graph-excluded）
│   ├── sources/                # 来源摘要页
│   ├── concepts/               # 概念/思想/模式
│   ├── entities/               # 人物/工具/机构/论文
│   ├── synthesis/              # 跨来源合成分析
│   └── templates/              # 页面模板
├── outputs/                    # 查询答案、lint 报告
└── scripts/
    └── lint_check.py           # Wiki 健康检查脚本
```

## 🔧 9 项健康检查

| # | 检查项 | 说明 |
|:---|:---|:---|
| 1 | YAML frontmatter 合法性 | 所有 .md 文件是否有合法 frontmatter |
| 2 | Broken Wikilinks | `[[xxx]]` 引用了不存在的页面 |
| 3 | Index 一致性 | index.md 中标记的文件是否都实际存在 |
| 4 | Stub 页面 | 正文少于 100 字的空壳页面 |
| 5 | 近重复概念名称 | slug Jaccard 相似度 > 0.7 |
| 6 | SHA-256 完整性 | 原始文件哈希比对，检测篡改 |
| 7 | Stale 页面 | 超过 domain_volatility 时效阈值 |
| 8 | 跨语言重复 | aliases 重叠 + URL 相似度 |
| 9 | Wikilink 格式规范 | 检测中文/大写/下划线等违规格式 |

## 📂 项目结构

```
LLMwiki-for-Obsidian/
├── SKILL.md                    # Skill 定义文件
├── agent_template.md           # Agent 行为契约模板
├── references/                 # 操作参考文档
│   ├── create-vault.md        # 创建仓库说明
│   ├── Ingest.md              # 摄入来源说明
│   ├── Query.md               # 查询说明
│   ├── Lint.md                # 健康检查说明
│   ├── lint_check.md          # Python 脚本文档
│   ├── merge.md               # 合并说明
│   ├── reflect.md             # 反思合成说明
│   └── add-question.md        # 添加问题说明
└── scripts/                   # Python 脚本
    ├── lint_check.py          # 主入口
    └── checkers/              # 检查器模块
        ├── base.py
        ├── utils.py
        ├── frontmatter_validity.py
        ├── broken_wikilinks.py
        ├── index_consistency.py
        ├── stub_pages.py
        ├── near_duplicate_slugs.py
        ├── sha256_integrity.py
        ├── stale_pages.py
        ├── cross_language_duplicates.py
        └── wikilink_format.py
```

## 🔗 相关项目

- [Obsidian](https://obsidian.md/) - 知识库管理工具
- [qmd](https://github.com/tobi/qmd) - 快速 Markdown 索引和查询工具
- [Andrej Karpathy's LLM Wiki](https://karpathy.ai/) - 设计思路来源



## 📄 许可证

MIT License
