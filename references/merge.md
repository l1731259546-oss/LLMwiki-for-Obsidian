# merge - 合并重复概念/实体

## 功能说明

合并重复的概念或实体页面，处理同语言和跨语言合并，确保 wikilinks 不中断。

## 同语言合并流程

1. **与用户确认合并方案**（绝不自动合并）
2. **主 slug 保留**，被合并页面的 wikilinks 全部更新
3. **被合并文件**替换为重定向文件，内容：`redirect: [[wiki/concepts/主slug]]`
4. **log.md 记录**：`YYYY-MM-DD | merge | [旧slug] → [主slug]`

## 跨语言合并专项流程（区别于同语言 MERGE）

1. **主 slug 保留英文**
2. **aliases 取两个页面的并集**
3. **Key Points / Sources / Evolution Log** 按并集+去重合并
4. **My Position 若两页都有**，先向用户展示对比后再合并
5. **被合并的旧 slug 文件保留为 redirect 文件**（确保旧 wikilinks 不 broken）
6. **log.md 记录**：`YYYY-MM-DD | merge | [旧slug] → [主slug]（跨语言合并）`

## 检查事项

- 合并后需要扫描所有文件，检查是否还有指向旧 slug 的链接
- 如果有，建议用户更新或自动更新（需用户确认）
- 更新 concept 页面的 source_count 和 confidence

## 何时调用

- lint 报告发现近重复概念时
- 用户发现重复概念要求合并时
- 跨语言摄入发现同一概念已有页面时