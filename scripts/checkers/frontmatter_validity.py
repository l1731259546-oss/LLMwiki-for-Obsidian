"""
1. YAML frontmatter 合法性检查
所有 wiki/ 下的 .md 文件是否有合法 YAML frontmatter（含 type 和 date）
"""

from .base import BaseChecker
from .utils import read_file, parse_frontmatter
from typing import List, Dict


class FrontmatterValidityChecker(BaseChecker):
    """YAML frontmatter 合法性检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        md_files = list(self.wiki_dir.rglob("*.md"))
        
        for md_file in md_files:
            content = read_file(md_file)
            if content is None:
                self.add_error(f"无法读取文件 {md_file}")
                continue
            
            frontmatter, _ = parse_frontmatter(content)
            rel_path = md_file.relative_to(self.base_dir)
            
            if frontmatter is None:
                issues.append({
                    "file": str(rel_path),
                    "issue": "缺少合法 YAML frontmatter"
                })
                continue
            
            if 'type' not in frontmatter:
                issues.append({
                    "file": str(rel_path),
                    "issue": "frontmatter 缺少 'type' 字段"
                })
            
            
            if 'date' not in frontmatter:
                issues.append({
                    "file": str(rel_path),
                    "issue": "frontmatter 缺少 'date' 字段"
                })
        
        
        return issues
