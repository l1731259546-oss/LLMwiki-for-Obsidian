"""
2. Broken Wikilinks 检查
[[xxx]] 引用了不存在的页面
"""

from .base import BaseChecker
from .utils import read_file, extract_wikilinks
from typing import List, Dict, Set


class BrokenWikilinksChecker(BaseChecker):
    """Broken Wikilinks 检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        md_files = list(self.wiki_dir.rglob("*.md"))
        
        # 预计算所有存在的 wiki 页面（不包含扩展名）
        existing_pages: Set[str] = set()
        for md_file in md_files:
            if md_file.suffix == '.md':
                rel = md_file.relative_to(self.wiki_dir)
                # wikilink 使用 slug（不包含 .md）
                slug = str(rel.with_suffix(''))
                existing_pages.add(slug.replace('\\', '/'))
        
        
        for md_file in md_files:
            content = read_file(md_file)
            if content is None:
                self.add_error(f"无法读取文件 {md_file}")
                continue
            
            wikilinks = extract_wikilinks(content)
            rel_path = md_file.relative_to(self.base_dir)
            
            for link in wikilinks:
                # 处理路径格式
                link_clean = link.replace('\\', '/').strip('/')
                # 检查文件是否存在
                found = False
                candidate_paths = [
                    self.wiki_dir / f"{link_clean}.md",
                    self.wiki_dir / link_clean / "index.md",
                    self.base_dir / f"{link_clean}.md",
                ]
                for candidate in candidate_paths:
                    if candidate.exists():
                        found = True
                        break
                
                if not found and link_clean in existing_pages:
                    found = True
                
                if not found:
                    issues.append({
                        "file": str(rel_path),
                        "broken_link": link
                    })
        
        
        return issues
