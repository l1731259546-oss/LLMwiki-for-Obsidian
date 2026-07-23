"""
6. SHA-256 完整性检查
raw 文件哈希与 source 页 raw_sha256 字段比对（⚠ SOURCE MODIFIED）
"""

from .base import BaseChecker
from .utils import read_file, parse_frontmatter, compute_sha256
from typing import List, Dict


class Sha256IntegrityChecker(BaseChecker):
    """SHA-256 完整性检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        sources_dir = self.wiki_dir / "sources"
        
        if not sources_dir.exists():
            return issues
        
        source_files = list(sources_dir.glob("*.md"))
        
        for source_file in source_files:
            content = read_file(source_file)
            if content is None:
                self.add_error(f"无法读取文件 {source_file}")
                continue
            
            frontmatter, _ = parse_frontmatter(content)
            if not frontmatter:
                continue
            
            if 'raw_file' not in frontmatter or 'raw_sha256' not in frontmatter:
                continue
            
            raw_file_rel = frontmatter['raw_file']
            expected_hash = frontmatter['raw_sha256'].strip()
            
            raw_file = self.base_dir / raw_file_rel
            if not raw_file.exists():
                rel_source = source_file.relative_to(self.base_dir)
                issues.append({
                    "source_file": str(rel_source),
                    "raw_file": raw_file_rel,
                    "issue": "原始文件不存在"
                })
                continue
            
            actual_hash = compute_sha256(raw_file)
            if actual_hash is None:
                self.add_error(f"无法计算哈希 {raw_file}")
                continue
            
            if actual_hash != expected_hash:
                rel_source = source_file.relative_to(self.base_dir)
                issues.append({
                    "source_file": str(rel_source),
                    "raw_file": raw_file_rel,
                    "expected_hash": expected_hash,
                    "actual_hash": actual_hash,
                    "issue": "SOURCE MODIFIED：原始文件已修改"
                })
        
        
        return issues
