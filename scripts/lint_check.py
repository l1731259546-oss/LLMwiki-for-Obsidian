"""
LLMwiki Wiki 健康检查脚本
执行 9 项检查，输出 JSON 结果和 Markdown 报告

架构：模块化设计，每个检查独立模块

检查清单：
1. YAML frontmatter 合法性：所有 wiki/ 下的 .md 文件是否有合法 YAML frontmatter（含 type 和 date）
2. Broken Wikilinks：[[xxx]] 引用了不存在的页面
3. Index 一致性：wiki/index.md 中标记的文件是否都实际存在
4. Stub 页面：正文少于 100 字的空壳页面
5. 近重复概念名称：slug 名称 Jaccard 相似度 > 0.7 的 concept 页对
6. SHA-256 完整性：raw 文件哈希与 source 页 raw_sha256 字段比对（⚠ SOURCE MODIFIED）
7. Stale 页面：超过 domain_volatility 时效阈值（high=90天, medium=180天, low=365天）
8. 跨语言重复：source URL 相似度检测 + 不同 concept 页的 aliases 字段重叠检测
9. Wikilink 格式规范：检测非英文小写连字符格式的 wikilink（如中文词汇 [[价值投资]]）及别名断链
"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 导入模块化检查器
from checkers.base import BaseChecker
from checkers.frontmatter_validity import FrontmatterValidityChecker
from checkers.broken_wikilinks import BrokenWikilinksChecker
from checkers.index_consistency import IndexConsistencyChecker
from checkers.stub_pages import StubPagesChecker
from checkers.near_duplicate_slugs import NearDuplicateSlugsChecker
from checkers.sha256_integrity import Sha256IntegrityChecker
from checkers.stale_pages import StalePagesChecker
from checkers.cross_language_duplicates import CrossLanguageDuplicatesChecker
from checkers.wikilink_format import WikilinkFormatChecker


class LintChecker:
    """主协调类，组合所有检查器"""
    
    def __init__(self, base_dir: str):
        """
        初始化检查器
        
        Args:
            base_dir: 知识库根目录（包含 wiki/ raw/ 的路径）
        """
        self.base_dir = Path(base_dir).resolve()
        self.wiki_dir = self.base_dir / "wiki"
        self.raw_dir = self.base_dir / "raw"
        
        # 初始化所有检查器
        self.checkers: List[BaseChecker] = [
            FrontmatterValidityChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            BrokenWikilinksChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            IndexConsistencyChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            StubPagesChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            NearDuplicateSlugsChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            Sha256IntegrityChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            StalePagesChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            CrossLanguageDuplicatesChecker(self.base_dir, self.wiki_dir, self.raw_dir),
            WikilinkFormatChecker(self.base_dir, self.wiki_dir, self.raw_dir),
        ]
    
    def run_all_checks(self) -> Dict:
        """运行所有检查，返回结果"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "errors": [],
        }
        
        # 收集所有检查结果
        for checker in self.checkers:
            issues = checker.check()
            check_name = checker.__class__.__name__[:-7].lower()
            results["checks"][check_name] = issues
            # 收集 checker 自身的错误
            results["errors"].extend(checker.errors)
        
        
        # 计算统计
        total_issues = 0
        for check_name, check_issues in results["checks"].items():
            total_issues += len(check_issues)
        
        results["summary"] = {
            "total_files_checked": len(list(self.wiki_dir.rglob("*.md"))),
            "total_issues_found": total_issues + len(results["errors"]),
            "errors": len(results["errors"]),
            "warnings": total_issues,
        }
        
        return results
    
    def write_report(self, results: Dict, output_path: str) -> None:
        """将结果写入 Markdown 报告"""
        check_names = {
            "frontmattervalidity": "1. YAML frontmatter 合法性",
            "brokenwikilinks": "2. Broken Wikilinks",
            "indexconsistency": "3. Index 一致性",
            "stubpages": "4. Stub 空壳页面",
            "nearduplicateslugs": "5. 近重复概念名称",
            "sha256integrity": "6. SHA-256 完整性",
            "stalepages": "7. Stale 过时页面",
            "crosslanguageduplicates": "8. 跨语言重复检测",
            "wikilinkformat": "9. Wikilink 格式规范",
        }
        
        lines = []
        lines.append("---")
        lines.append("type: lint-report")
        lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("graph-excluded: true")
        lines.append("")
        lines.append(f"# Lint Report - {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- 检查文件总数: **{results['summary']['total_files_checked']}**")
        lines.append(f"- 发现问题: **{results['summary']['total_issues_found']}**")
        lines.append(f"  - 错误: {results['summary']['errors']}")
        lines.append(f"  - 警告: {results['summary']['warnings']}")
        lines.append("")
        
        if results['errors']:
            lines.append("## Script Errors")
            lines.append("")
            for err in results['errors']:
                lines.append(f"- ❌ {err}")
            lines.append("")
        
        lines.append("## Details by Check")
        lines.append("")
        
        for check_key, check_issues in results["checks"].items():
            check_display = check_names.get(check_key, check_key)
            lines.append(f"### {check_display}")
            lines.append("")
            
            if len(check_issues) == 0:
                lines.append("✅ 无问题")
                lines.append("")
                continue
            
            for issue in check_issues:
                if check_key == "frontmattervalidity":
                    lines.append(f"- `{issue['file']}`: {issue['issue']}")
                elif check_key == "brokenwikilinks":
                    lines.append(f"- `{issue['file']}`: 断链 → `[[{issue['broken_link']}]]`")
                elif check_key == "indexconsistency":
                    if 'missing_file' in issue:
                        lines.append(f"- `{issue['file']}`: 缺失文件 → {issue['missing_file']}")
                    else:
                        lines.append(f"- `{issue['file']}`: {issue['issue']}")
                elif check_key == "stubpages":
                    lines.append(f"- `{issue['file']}`: 正文字符数过少 ({issue['character_count']} 字)")
                elif check_key == "nearduplicateslugs":
                    lines.append(f"- `{issue['slug1']}` 与 `{issue['slug2']}`: 相似度 {issue['similarity']}")
                elif check_key == "sha256integrity":
                    lines.append(f"- ⚠ `{issue['source_file']}`: {issue['issue']} ({issue['raw_file']})")
                elif check_key == "stalepages":
                    lines.append(f"- `{issue['file']}`: {issue['days_since_review']} 天未复审（阈值 {issue['threshold_days']} 天）")
                elif check_key == "crosslanguageduplicates":
                    if issue['type'] == 'alias_overlap':
                        lines.append(f"- `{issue['concept1']}` 与 `{issue['concept2']}`: Aliases 重叠 {issue['overlapping_aliases']}")
                    else:
                        lines.append(f"- `{issue['source1']}` 与 `{issue['source2']}`: URL 相似度 {issue['similarity']}")
                elif check_key == "wikilinkformat":
                    lines.append(f"- `{issue['file']}`: `[[{issue['wikilink']}]]` → {issue['violation']}")
                lines.append("")
        
        lines.append("## Recommendations")
        lines.append("")
        if results['summary']['total_issues_found'] == 0:
            lines.append("🎉 一切正常，没有发现问题！")
        else:
            lines.append("- 建议按优先级修复上述问题")
            lines.append("- 先修复错误（如 broken wikilinks），再处理警告")
            lines.append("- 近重复概念建议使用 `merge` 操作合并")
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"Lint 报告已写入: {output_path}")
    
    def print_summary(self, results: Dict) -> None:
        """在控制台打印摘要"""
        print("=" * 60)
        print("LLMwiki Lint Check Summary")
        print(f"Timestamp: {results['timestamp']}")
        print("=" * 60)
        print(f"Total files checked: {results['summary']['total_files_checked']}")
        print(f"Total issues found: {results['summary']['total_issues_found']}")
        print(f"  Errors: {results['summary']['errors']}")
        print(f"  Warnings: {results['summary']['warnings']}")
        print("=" * 60)
        
        for checker in self.checkers:
            check_name = checker.__class__.__name__[:-7].lower()
            if check_name in results["checks"]:
                issues = results["checks"][check_name]
                if len(issues) > 0:
                    print(f"{check_name}: {len(issues)} issues")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='LLMwiki 健康检查脚本')
    parser.add_argument('base_dir', help='知识库根目录路径')
    parser.add_argument('--output', '-o', help='输出报告路径 (默认: outputs/lint-YYYY-MM-DD.md)')
    
    args = parser.parse_args()
    
    if not args.output:
        today = datetime.now().strftime('%Y-%m-%d')
        args.output = os.path.join(args.base_dir, f'outputs/lint-{today}.md')
    
    checker = LintChecker(args.base_dir)
    results = checker.run_all_checks()
    checker.write_report(results, args.output)
    checker.print_summary(results)
    
    if results['summary']['total_issues_found'] > 0:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
