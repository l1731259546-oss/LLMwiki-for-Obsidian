"""
4. Stub 页面检查
正文少于 100 字的空壳页面
"""

import re
from .base import BaseChecker
from .utils import read_file, parse_frontmatter
from typing import List, Dict


class StubPagesChecker(BaseChecker):
    """Stub 页面检查"""
    
    def __init__(self, base_dir, wiki_dir, raw_dir, min_chars: int = 100):
        super().__init__(base_dir, wiki_dir, raw_dir)
        self.min_chars = min_chars
    
    def check(self) -> List[Dict]:
        issues = []
        md_files = list(self.wiki_dir.rglob("*.md"))
        
        # 排除系统文件
        system_files = ['index.md', 'log.md', 'overview.md', 'QUESTIONS.md']
        
        for md_file in md_files:
            if md_file.name in system_files:
                continue
            
            content = read_file(md_file)
            if content is None:
                self.add_error(f"无法读取文件 {md_file}")
                continue
            
            _, body = parse_frontmatter(content)
            # 计算正文字符数（去除空白行）
            body_clean = re.sub(r'\s+', ' ', body).strip()
            char_count = len(body_clean)
            
            if char_count < self.min_chars:
                rel_path = md_file.relative_to(self.base_dir)
                issues.append({
                    "file": str(rel_path),
                    "character_count": char_count
                })
        
        
        return issues
