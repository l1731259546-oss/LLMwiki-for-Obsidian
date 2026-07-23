# query - 基于知识库回答问题

## 功能说明

回答用户问题，基于 wiki 中已有的知识合成答案，写入 outputs。


## 执行要求1
调用
`/obsidian-bases`
`/obsidian-cli`
`/obsidian-defuddle`
`/obsobsidian-json-canvas`
操控obsidian客户端
## 执行要求2
使用qmd 索引


## 执行流程

1. **问题解析**
   - 提取问题核心概念
   - 识别相关的概念/实体/来源

2. **检索相关页面**
   - 通过 qmd 搜索相关概念
   - 读取所有相关页面的完整内容
   - 收集所有相关来源信息

3. **合成答案**
   - 整合不同来源的观点
   - 标注不同来源的分歧
   - 说明 confidence 水平
   - 如果信息不足，明确指出

4. **写入输出**
   - 创建 `outputs/query-YYYY-MM-DD-topic-slug.md`
   - frontmatter 包含：`type: query-result`, `date`, `question`, `tags`, `graph-excluded: true`
   - 正文结构：
   ```
     ## Question
     ## Answer
     ## Sources Referenced（wikilinks 列表）
     ## Confidence Notes
     ## Open Follow-up Questions
   ```

5. **更新日志**
   - 在 `wiki/log.md` 追加：`YYYY-MM-DD HH:MM | query | [问题简述]`

## 何时调用

- 用户明确提出问题，希望基于已有知识库回答时
- 新摄入的来源可能回答了某个开放问题，用户确认后