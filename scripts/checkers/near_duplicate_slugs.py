"""
5. 近重复概念名称检查
slug 名称 Jaccard 相似度 > 0.7 的 concept 页对
优化：添加前缀剪枝减少 O(n²) 比较次数
"""

from .base import BaseChecker
from .utils import jaccard_similarity, group_slugs_by_prefix
from typing import List, Dict


class NearDuplicateSlugsChecker(BaseChecker):
    """近重复概念名称检查"""
    
    def __init__(self, base_dir, wiki_dir, raw_dir, threshold: float = 0.7, max_slugs: int = 500):
        super().__init__(base_dir, wiki_dir, raw_dir)
        self.threshold = threshold
        self.max_slugs = max_slugs  # O(n²) 保护阈值
    
    def check(self) -> List[Dict]:
        issues = []
        concepts_dir = self.wiki_dir / "concepts"
        
        if not concepts_dir.exists():
            return issues
        
        concept_files = list(concepts_dir.glob("*.md"))
        slugs = [f.stem for f in concept_files]
        
        # O(n²) 优化：如果 slug 数量太大，添加警告并只检查前 N 个
        if len(slugs) > self.max_slugs:
            self.add_error(
                f"concept 数量 ({len(slugs)}) 超过阈值 {self.max_slugs}，"
                "仅检查前 {self.max_slugs} 个 slug 以避免过长时间"
            )
            slugs = slugs[:self.max_slugs]
        
        
        # 前缀剪枝优化：只比较相同前缀的 slug，大大减少比较次数
        groups = group_slugs_by_prefix(slugs)
        
        for _, group_slugs in groups.items():
            # 只在组内两两比较，不同前缀的slug相似度不可能太高
            n = len(group_slugs)
            for i in range(n):
                for j in range(i + 1, n):
                    similarity = jaccard_similarity(group_slugs[i], group_slugs[j])
                    if similarity > self.threshold:
                        issues.append({
                            "slug1": group_slugs[i],
                            "slug2": group_slugs[j],
                            "similarity": round(similarity, 3)
                        })
        
        
        return issues
