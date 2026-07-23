# lint - Wiki 健康检查

## 功能说明

运行完整的 Wiki 健康检查，使用 `scripts/lint_check.py` 执行 9 项检查，生成报告并询问用户是否修复问题。

## 执行步骤

1. **运行 scripts/lint_check.py**（包含 9 项检查，模块化架构，每个检查独立模块）
2. **将报告写入** `outputs/lint-YYYY-MM-DD.md`（frontmatter 含 `graph-excluded: true`）
3. **执行 qmd status**，对比索引文件数与 wiki/ 实际 .md 文件数（排除系统文件）；若索引落后则执行 `qmd add wiki/`，在报告中记录
4. **向用户展示摘要**并询问是否修复

## 架构说明

自 v2.0 起采用模块化架构：

- `scripts/lint_check.py` - 主入口和协调类
- `scripts/checkers/base.py` - 基础接口定义
- `scripts/checkers/utils.py` - 共享工具函数
- `scripts/checkers/*.py` - 每个检查独立模块

### 性能优化

对于 O(n²) 两两比较算法（近重复检测、跨语言重复检测）添加了**阈值保护**：
- 当 concept 数量超过 500 时，只检查前 500 个并发出警告
- 使用**前缀剪枝**优化，只比较相同前缀的 slug，大大减少比较次数
- 这样在大规模知识库中也能保持合理的运行时间

## 9 项检查清单

| 编号 | 检查项 | 说明 |
| :--- | :--- | :--- |
| 1 | YAML frontmatter 合法性 | 所有 wiki/ 下的 .md 文件是否有合法 YAML frontmatter（含 type 和 date） |
| 2 | Broken Wikilinks | 检测 `[[xxx]]` 引用了不存在的页面 |
| 3 | Index 一致性 | wiki/index.md 中标记的文件是否都实际存在 |
| 4 | Stub 页面 | 正文少于 100 字的空壳页面 |
| 5 | 近重复概念名称 | slug 名称 Jaccard 相似度 > 0.7 的 concept 页对 |
| 6 | SHA-256 完整性 | raw 文件哈希与 source 页 raw_sha256 字段比对，检测 ⚠ SOURCE MODIFIED |
| 7 | Stale 页面 | 超过 domain_volatility 时效阈值（high=90天, medium=180天, low=365天） |
| 8 | 跨语言重复 | source URL 相似度检测 + 不同 concept 页的 aliases 字段重叠检测 |
| 9 | Wikilink 格式规范 | 检测非英文小写连字符格式的 wikilink（如中文词汇 `[[价值投资]]`）及别名断链 |

## 输出报告格式

```markdown
---
type: lint-report
date: YYYY-MM-DD
graph-excluded: true
---

# Lint Report - YYYY-MM-DD

## Summary

- Total files checked: X
- Issues found: Y
  - Errors: E
  - Warnings: W

## Details by check

### 1. YAML frontmatter 合法性
...

### 2. Broken Wikilinks
...

...

## Recommendations
- 建议修复项目符号列表
```

## 何时调用

- 定期维护知识库时
- 完成批量摄入后
- 用户明确要求检查知识库健康时