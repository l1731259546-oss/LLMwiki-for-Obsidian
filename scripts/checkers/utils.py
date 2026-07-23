"""
共享工具函数
"""

import re
import hashlib
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Set


def read_file(file_path: Path) -> Optional[str]:
    """读取文件内容，处理编码问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """解析 YAML frontmatter，返回 (frontmatter_dict, 正文内容)"""
    if not content.startswith('---\n'):
        return None, content
    
    # 查找第二个 ---
    # 允许 --- 后直接跟正文，不需要强制换行
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, content
    
    try:
        import yaml
        frontmatter = yaml.safe_load(match.group(1))
        content_body = content[match.end():]
        return frontmatter, content_body
    except Exception as e:
        return None, content


def compute_sha256(file_path: Path) -> Optional[str]:
    """计算文件 SHA-256 哈希"""
    try:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return None


def extract_wikilinks(content: str) -> List[str]:
    """从内容中提取所有 wikilink 目标"""
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)
    return [link.strip() for link in matches]


def jaccard_similarity(a: str, b: str) -> float:
    """计算两个字符串的 Jaccard 相似度"""
    set_a = set(a)
    set_b = set(b)
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def group_slugs_by_prefix(slugs: List[str], prefix_len: int = 3) -> Dict[str, List[str]]:
    """按前缀分组 slug，用于 O(n²) 剪枝"""
    groups: Dict[str, List[str]] = {}
    for slug in slugs:
        prefix = slug[:prefix_len]
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(slug)
    return groups
