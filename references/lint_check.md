# lint_check - Python 检查脚本

## 脚本位置

```
.trae/skills/LLMwiki-for-Obsidian/scripts/
├── lint_check.py              # 主入口和协调类
├── checkers/
│   ├── base.py               # 基础接口定义 (BaseChecker)
│   ├── utils.py              # 共享工具函数 (read_file, parse_frontmatter, etc.)
│   ├── frontmatter_validity.py
│   ├── broken_wikilinks.py
│   ├── index_consistency.py
│   ├── stub_pages.py
│   ├── near_duplicate_slugs.py
│   ├── sha256_integrity.py
│   ├── stale_pages.py
│   ├── cross_language_duplicates.py
│   └── wikilink_format.py
```

## 功能说明

Python 脚本，执行 9 项具体的 Wiki 健康检查，输出 JSON 结果供后续处理。

**架构改进**：模块化设计，每个检查独立一个模块，提高可维护性和可测试性。

**性能优化**：对 O(n²) 算法添加阈值保护和前缀剪枝，大规模知识库运行更稳定。

## 9 项检查

按照要求执行以下 9 项检查：

### 1. YAML frontmatter 合法性
- 扫描所有 `wiki/**/*.md` 文件
- 检查是否有合法的 YAML frontmatter（以 `---` 开头和结尾）
- **bug 修复**：支持 `---` 后直接跟正文（不需要强制换行）
- 检查是否包含 `type` 和 `date` 字段
- 输出：缺少 frontmatter 或缺少必填字段的文件列表

### 2. Broken Wikilinks
- 使用正则表达式提取所有 `[[...]]` wikilink
- 解析 wikilink 目标（支持 `[[目标]]` 和 `[[目标|显示]]` 格式）
- 检查对应的文件是否存在于 wiki/ 目录
- 输出：断链列表（文件 → 断链）

### 3. Index 一致性
- 读取 `wiki/index.md`
- 提取所有 wikilink
- 检查每个链接对应的文件是否实际存在
- 输出：索引中引用但不存在的文件列表

### 4. Stub 页面
- 计算每个页面正文字符数（排除 frontmatter）
- 标记正文少于 100 字的页面
- 排除系统文件（index, log, overview, QUESTIONS 等）
- 输出：stub 页面列表

### 5. 近重复概念名称
- 获取所有 `wiki/concepts/*.md` 的 slug
- **优化**：前缀分组剪枝，只比较相同前缀的 slug
- **优化**：数量超过 500 时截断并警告，避免 O(n²) 过慢
- 计算两两之间的 Jaccard 相似度
- 输出相似度 > 0.7 的概念对

### 6. SHA-256 完整性
- 遍历所有 `wiki/sources/*.md`
- 读取 frontmatter 中的 `raw_file` 和 `raw_sha256`
- 重新计算原始文件的 SHA-256
- 与存储的哈希比对，检测是否被修改
- 输出：SOURCE MODIFIED 文件列表

### 7. Stale 页面
- 对于 `wiki/concepts/*.md`，读取 `last_reviewed` 和 `domain_volatility`
- 根据 volatility 计算阈值：
  - high = 90 天
  - medium = 180 天
  - low = 365 天
- 检查距今天数是否超过阈值
- 输出：stale 页面列表

### 8. 跨语言重复
- **优化**：concept 和 source 数量超过阈值时截断并警告
- 对所有 concept 页，收集 aliases 列表
- 检查不同页面之间的 aliases 是否有重叠
- 对 source 页，检查 URL 是否有相似性
- 输出：可能重复的页面对

### 9. Wikilink 格式规范
- 提取所有 wikilink
- 检查是否符合「英文小写连字符」格式
- 检测：中文词汇、驼峰、下划线等违规格式
- 输出：违规 wikilink 列表（文件 → 违规链接）

## 使用方法

```python
from lint_check import LintChecker

checker = LintChecker("path/to/knowledge-base")
results = checker.run_all_checks()
checker.write_report(results, "outputs/lint-YYYY-MM-DD.md")
```

## 输出格式

返回 JSON 格式结果：

```json
{
  "timestamp": "2026-07-20T...",
  "summary": {
    "total_files": 100,
    "issues_found": 10,
    "errors": 3,
    "warnings": 7
  },
  "checks": {
    "frontmatter_validity": [...],
    "broken_wikilinks": [...],
    ...
  }
}
```

## 依赖

- Python 3.8+
- PyYAML
- hashlib（内置）
- difflib（内置）