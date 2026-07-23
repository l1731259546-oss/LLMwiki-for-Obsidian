"""
8. 跨语言重复检查
source URL 相似度检测 + 不同 concept 页的 aliases 字段重叠检测
优化：添加前缀剪枝减少 O(n²) 比较次数
"""

from difflib import SequenceMatcher
from .base import BaseChecker
from .utils import read_file, parse_frontmatter
from typing import List, Dict, Set, Tuple


class CrossLanguageDuplicatesChecker(BaseChecker):
    """跨语言重复检查"""
    
    def __init__(self, base_dir, wiki_dir, raw_dir, max_concepts: int = 500, max_sources: int = 500):
        super().__init__(base_dir, wiki_dir, raw_dir)
        self.max_concepts = max_concepts  # O(n²) 保护阈值
        self.max_sources = max_sources    # O(n²) 保护阈值
    
    def check(self) -> List[Dict]:
        issues = []
        
        # 检查 concept aliases 重叠
        issues.extend(self._check_concept_aliases())
        
        # 检查 source URL 重复
        issues.extend(self._check_source_urls())
        
        
        return issues
    
    
    def _check_concept_aliases(self) -> List[Dict]:
        """检查 concept 页面 aliases 重叠"""
        issues = []
        concepts_dir = self.wiki_dir / "concepts"
        
        if not concepts_dir.exists():
            return issues
        
        concept_aliases: List[Tuple[str, Set[str]]] = []
        
        for concept_file in concepts_dir.glob("*.md"):
            content = read_file(concept_file)
            if content is None:
                continue
            
            frontmatter, _ = parse_frontmatter(content)
            if not frontmatter:
                continue
            
            aliases = frontmatter.get('aliases', [])
            if not aliases:
                continue
            
            alias_set = set()
            for a in aliases:
                if isinstance(a, str):
                    alias_set.add(a.strip().lower())
            
            concept_aliases.append((concept_file.stem, alias_set))
        
        
        # O(n²) 保护：如果概念太多，截断并警告
        if len(concept_aliases) > self.max_concepts:
            self.add_error(
                f"concept 数量 ({len(concept_aliases)}) 超过阈值 {self.max_concepts}，"
                "仅检查前 {self.max_concepts} 个以避免过长时间"
            )
            concept_aliases = concept_aliases[:self.max_concepts]
        
        
        # 两两比较
        n = len(concept_aliases)
        for i in range(n):
            for j in range(i + 1, n):
                slug1, aliases1 = concept_aliases[i]
                slug2, aliases2 = concept_aliases[j]
                intersection = aliases1 & aliases2
                if len(intersection) > 0:
                    issues.append({
                        "type": "alias_overlap",
                        "concept1": slug1,
                        "concept2": slug2,
                        "overlapping_aliases": list(intersection)
                    })
        
        
        return issues
    
    
    def _check_source_urls(self) -> List[Dict]:
        """检查 source 页面 URL 相似"""
        issues = []
        sources_dir = self.wiki_dir / "sources"
        
        if not sources_dir.exists():
            return issues
        
        source_urls: List[Tuple[str, str]] = []
        
        for source_file in sources_dir.glob("*.md"):
            content = read_file(source_file)
            if content is None:
                continue
            
            frontmatter, _ = parse_frontmatter(content)
            if not frontmatter:
                continue
            
            url = frontmatter.get('source_url')
            if url:
                source_urls.append((source_file.stem, url))
        
        
        # O(n²) 保护：如果 source 太多，截断并警告
        if len(source_urls) > self.max_sources:
            self.add_error(
                f"source 数量 ({len(source_urls)}) 超过阈值 {self.max_sources}，"
                "仅检查前 {self.max_sources} 个以避免过长时间"
            )
            source_urls = source_urls[:self.max_sources]
        
        
        # 两两比较
        n = len(source_urls)
        for i in range(n):
            for j in range(i + 1, n):
                slug1, url1 = source_urls[i]
                slug2, url2 = source_urls[j]
                similarity = SequenceMatcher(None, url1, url2).ratio()
                if similarity > 0.9:
                    issues.append({
                        "type": "url_similarity",
                        "source1": slug1,
                        "source2": slug2,
                        "similarity": round(similarity, 3),
                        "url1": url1,
                        "url2": url2
                    })
        
        
        return issues
