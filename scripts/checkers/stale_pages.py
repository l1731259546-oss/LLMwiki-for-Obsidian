"""
7. Stale 页面检查
超过 domain_volatility 时效阈值（high=90天, medium=180天, low=365天）
"""

from datetime import datetime
from .base import BaseChecker
from .utils import read_file, parse_frontmatter
from typing import List, Dict


class StalePagesChecker(BaseChecker):
    """Stale 页面检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        concepts_dir = self.wiki_dir / "concepts"
        
        if not concepts_dir.exists():
            return issues
        
        volatility_thresholds = {
            'high': 90,
            'medium': 180,
            'low': 365,
        }
        
        today = datetime.now().date()
        concept_files = list(concepts_dir.glob("*.md"))
        
        for concept_file in concept_files:
            content = read_file(concept_file)
            if content is None:
                self.add_error(f"无法读取文件 {concept_file}")
                continue
            
            frontmatter, _ = parse_frontmatter(content)
            if not frontmatter:
                continue
            
            # 获取 last_reviewed
            last_reviewed_str = frontmatter.get('last_reviewed')
            if not last_reviewed_str:
                # 使用 updated 或 date
                last_reviewed_str = frontmatter.get('updated') or frontmatter.get('date')
            
            if not last_reviewed_str:
                continue
            
            # 获取 volatility
            volatility = frontmatter.get('domain_volatility', 'medium')
            threshold_days = volatility_thresholds.get(volatility, 180)
            
            # 解析日期
            try:
                if isinstance(last_reviewed_str, str):
                    last_reviewed = datetime.strptime(last_reviewed_str[:10], '%Y-%m-%d').date()
                else:
                    continue
            except ValueError:
                continue
            
            days_since = (today - last_reviewed).days
            if days_since > threshold_days:
                rel_path = concept_file.relative_to(self.base_dir)
                issues.append({
                    "file": str(rel_path),
                    "last_reviewed": last_reviewed_str[:10],
                    "days_since_review": days_since,
                    "threshold_days": threshold_days,
                    "domain_volatility": volatility
                })
        
        
        return issues
