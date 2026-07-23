# create-vault - 创建 LLM Wiki 仓库

## 功能说明

从零创建完整的 LLM Wiki 仓库目录结构和所有系统文件、页面模板。


## 执行步骤
**执行完全部最后一步后检查是否每一步都成功执行**
### 1. 创建目录结构

创建以下目录：

```
wikiknowledge-base/
├── raw/articles/
├── raw/clippings/
├── raw/images/
├── raw/pdfs/
├── raw/notes/
├── raw/personal/
├── wiki/sources/
├── wiki/concepts/
├── wiki/entities/
├── wiki/synthesis/
├── wiki/templates/
├── outputs/
└── scripts/
```

### 2. 创建系统文件

#### wiki/index.md
- frontmatter: `type: system-index`, `graph-excluded: true`
- 正文包含：Sources 列表（按日期倒序）、Concepts 列表、Entities 列表、Recent Synthesis 列表、Outputs 列表

#### wiki/log.md
- frontmatter: `type: system-log`, `graph-excluded: true`
- 说明：仅追加操作日志，格式为「YYYY-MM-DD | 操作类型 | 说明」

#### wiki/overview.md
- frontmatter: `type: system-overview`, `graph-excluded: true`
- 包含：Knowledge Base Health Dashboard 表格（总来源数、高置信度概念数、开放问题数、Stale 页面数）

#### wiki/QUESTIONS.md
- frontmatter: `type: system-questions`, `graph-excluded: true`
- 包含：Open Questions 列表（checkbox 格式）、Resolved Questions 列表

### 3. 创建页面模板

#### wiki/templates/source-template.md
frontmatter 字段：
`type`, `title`, `date`, `source_url`, `domain`, `author`, `tags`, `processed`, `raw_file`, `raw_sha256`, `last_verified`, `possibly_outdated`, `language`, `canonical_source`
正文结构：
```
## Summary
## Key Points
## Concepts Extracted
## Entities Extracted
## Contradictions（与其他来源的分歧）
## My Notes
```

#### wiki/templates/personal-writing-template.md
frontmatter 字段：
`type: personal-writing`, `title`, `date`, `status(draft/published/deprecated)`, `topic_tags`, `confidence_at_writing(low/medium/high)`, `superseded_by`, `raw_file`, `raw_sha256`, `last_verified`, `tags`, `processed`
正文结构：
```
## Core Argument
## Key Claims
## Evidence Referenced
## Limitations
```

#### wiki/templates/concept-template.md
frontmatter 字段：
`type: concept`, `title`（中文主名称）, `date`, `updated`, `tags`, `source_count`, `confidence(low/medium/high)`, `domain_volatility(low/medium/high)`, `last_reviewed`, `aliases`（数组，存储中英文所有叫法）
正文结构：
```
## Definition（首行用「中文名（English Name）」格式）
## Key Points
## My Position
## Contradictions
## Sources（仅 wikilinks 列表）
## Evolution Log（每次更新追加一条）
```

#### wiki/templates/entity-template.md
frontmatter 字段：
`type: entity`, `title`, `date`, `tags`, `entity_type(person/tool/institution/paper)`, `aliases`
正文结构：
```
## Description
## Key Contributions
## Related Concepts
## Sources
```

#### wiki/templates/synthesis-template.md
frontmatter 字段：
`type: synthesis`, `title`, `date`, `tags`, `source_count`, `confidence`
正文结构：
```
## Thesis
## Evidence
## Counter-evidence（Stage 0 反向检验结果）
## Synthesis
## Confidence Notes
## Limitations
## Sources
```

### 4. 创建 Agent.md（行为契约）
用命令行复制`/agent_template.md`的内容到`/wiki/agent.md`


### 5. 初始化 qmd 索引
确保已经安装 qmd（npm install -g @tobi/qmd）
执行：
```bash
qmd add wiki/
qmd status
```

### 6. 验证
输出验证报告：
1. 目录结构树
2. AGENT.md 包含的章节列表
3. wiki/templates/ 下的模板文件列表
4. qmd status 输出
5. scripts/lint_check.py 包含的检查项列表

### 7. 全系统 Audit
请对当前知识库做一次完整的系统状态核查，逐项验证以下内容，
输出核查报告到 wiki/outputs/system-audit-YYYY-MM-DD.md：
#### 一、目录结构完整性
验证 raw/ 和 wiki/ 下所有子目录是否存在
#### 二、CLAUDE.md 关键规则覆盖（逐项输出是/否）
- [ ] Raw 层不可变原则
- [ ] INGEST 来源类型判断（personal-writing vs 外部来源）
- [ ] INGEST SHA-256 哈希记录规则
- [ ] INGEST 去重检测（含 canonical_source 译文检测）
- [ ] INGEST 概念名称对齐检查（aliases 匹配）
- [ ] INGEST QUESTIONS.md 匹配检查
- [ ] INGEST 缺少 frontmatter 的处理规则
- [ ] INGEST URL 直接输入的 defuddle 调用规则
- [ ] INGEST 最后一步执行 qmd update
- [ ] QUERY 使用 qmd query 优先（含 fallback）
- [ ] QUERY 来源溯源要求（追溯到 sources 页）
- [ ] QUERY Confidence Notes 输出要求
- [ ] QUERY 高价值答案持久化规则
- [ ] confidence: high 必须用户确认，禁止自动晋升
- [ ] LINT 运行 scripts/lint.py（9 项检查）
- [ ] LINT 执行 qmd 索引同步验证
- [ ] REFLECT Stage 0 反向检验
- [ ] REFLECT Stage 1 使用 qmd multi-get 批量扫描
- [ ] REFLECT Stage 3 Gap Analysis
- [ ] MERGE 跨语言合并专项流程（redirect 文件保留）
- [ ] Wikilink 格式铁律（英文小写连字符）
- [ ] Wikilink 禁止清单（系统文件不得被 wikilink）
- [ ] Wiki 语言规范（中文写作，英文 slug，aliases 跨语言）
- [ ] 系统文件隔离规则（graph-excluded: true）
- [ ] 文档维护规则（CLAUDE.md 更新时同步 USER_GUIDE.md）
#### 三、模板文件完整性（逐项验证必需字段）
- [ ] source-template.md 含 language / canonical_source
- [ ] personal-writing-template.md 含 type: personal-writing / confidence_at_writing
- [ ] concept-template.md 含 aliases / domain_volatility / last_reviewed / Evolution Log
- [ ] entity-template.md 含 aliases
- [ ] synthesis-template.md 含 Counter-evidence / Confidence Notes / Limitations
#### 四、系统文件隔离状态
- [ ] wiki/log.md 含 graph-excluded: true
- [ ] wiki/index.md 含 graph-excluded: true
- [ ] wiki/overview.md 含 graph-excluded: true
- [ ] wiki/QUESTIONS.md 含 graph-excluded: true
#### 五、scripts/lint.py 检查项（验证是否包含全部 9 项）
#### 六、qmd 状态
- qmd status 输出（索引文件数量）
- 执行一次测试查询，输出 top 3 结果
输出：✅ 通过 / ❌ 未通过（含缺失内容） / 建议修复优先级