"""
3. Index 一致性检查
wiki/index.md 中标记的文件是否都实际存在
"""

from .base import BaseChecker
from .utils import read_file, extract_wikilinks
from typing import List, Dict


class IndexConsistencyChecker(BaseChecker):
    """Index 一致性检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        index_path = self.wiki_dir / "index.md"
        
        if not index_path.exists():
            issues.append({
                "file": "wiki/index.md",
                "issue": "index.md 文件不存在"
            })
            return issues
        
        
        content = read_file(index_path)
        if content is None:
            self.add_error(f"无法读取文件 {index_path}")
            return issues
        
        
        wikilinks = extract_wikilinks(content)
        
        for link in wikilinks:
            link_clean = link.replace('\\', '/').strip('/')
            found = False
            candidate_paths = [
                self.wiki_dir / f"{link_clean}.md",
                self.base_dir / f"{link_clean}.md",
            ]
            for candidate in candidate_paths:
                if candidate.exists():
                    found = True
                    break
            
            if not found:
                issues.append({
                    "file": "wiki/index.md",
                    "missing_file": link_clean
                })
        
        
        return issues
