# reflect - 四阶段知识合成反思

## 功能说明

四阶段反思合成：反向检验 → 模式扫描 → 深度合成 → 缺口分析。发现跨来源模式、隐性关联、内容空白和矛盾对。

## 四阶段执行

### Stage 0（反向检验）

在生成任何合成结论之前，**主动搜索反驳证据**。

- 针对拟合成的命题，搜索 wiki 中所有持相反观点的来源
- 如果未找到反对来源，在合成页的 Limitations 节标注：
  > ⚠ 回音室风险：未找到反驳来源，结论可能存在确认偏差

### Stage 1（模式扫描）

使用 qmd 批量扫描：

```bash
qmd multi-get "wiki/concepts/*.md" -l 40
qmd multi-get "wiki/entities/*.md" -l 40
qmd multi-get "wiki/synthesis/*.md" -l 60
```

识别：
- 跨来源模式
- 隐性关联
- 内容空白
- 矛盾对

### Stage 2（深度合成）

对有证据支撑的候选项：
- 完整读取相关页面
- 写入 `wiki/synthesis/<topic>-synthesis.md`（使用 synthesis-template.md）

### Stage 3（Gap Analysis）

识别以下缺口：
- source_count = 1 且创建超过 30 天的孤立概念
- 多处提及但无独立页面的概念/实体（隐性盲区）
- 覆盖明显稀薄的主题领域

输出到 `outputs/gap-report-YYYY-MM-DD.md`（frontmatter 含 `graph-excluded: true`）

## 完成后更新

- 更新 `wiki/overview.md` 的 Health Dashboard
- 更新 `wiki/index.md`
- 追加 `wiki/log.md`：`YYYY-MM-DD HH:MM | reflect | gap analysis completed`

## 何时调用

- 定期（每月）进行知识库反思
- 摄入足够多新材料后
- 用户要求进行知识合成时