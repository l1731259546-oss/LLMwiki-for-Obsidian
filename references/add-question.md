# add-question - 添加开放问题

## 功能说明

将用户提出的开放问题添加到 wiki/QUESTIONS.md 队列中，供后续研究回答。

## 执行步骤

1. **将问题规范化**（提取核心疑问）
2. **追加到 wiki/QUESTIONS.md**（checkbox 格式）：
   ```
   - [ ] 问题内容（opened YYYY-MM-DD）
   ```
3. **追加 wiki/log.md**：`YYYY-MM-DD HH:MM | add-question | [问题简述]`

## 格式规范

### wiki/QUESTIONS.md 结构

- 第一部分：Open Questions（未回答），checkbox 格式
- 第二部分：Resolved Questions（已回答），链接到对应的合成页

示例：

```markdown
---
type: system-questions
graph-excluded: true
---

# Open Questions

- [ ] 如何有效管理个人知识体系？（opened 2026-07-20）
- [ ] LLM 在知识工作中的最佳实践是什么？（opened 2026-07-20）

# Resolved Questions

- [x] [什么是注意力机制](wiki/synthesis/attention-mechanism-synthesis.md)（answered 2026-07-15）
```

## 何时调用

- 用户提出一个暂无法回答的开放问题时
- 摄入过程中发现新的研究问题时