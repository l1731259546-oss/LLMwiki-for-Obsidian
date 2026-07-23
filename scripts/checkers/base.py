"""
Checker 基础接口
所有具体检查器都需要实现这个接口
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Optional


class CheckResult:
    """检查结果"""
    def __init__(self, check_name: str, issues: List[Dict]):
        self.check_name = check_name
        self.issues = issues
    
    def to_dict(self) -> Dict:
        return {
            "check_name": self.check_name,
            "issues": self.issues
        }


class BaseChecker(ABC):
    """所有检查器的抽象基类"""
    
    def __init__(self, base_dir: Path, wiki_dir: Path, raw_dir: Path):
        """
        初始化检查器
        
        Args:
            base_dir: 知识库根目录
            wiki_dir: wiki 目录
            raw_dir: raw 目录
        """
        self.base_dir = base_dir
        self.wiki_dir = wiki_dir
        self.raw_dir = raw_dir
        self.errors: List[str] = []
    
    @abstractmethod
    def check(self) -> List[Dict]:
        """
        执行检查
        
        Returns:
            问题列表，每个问题是一个字典，包含具体字段
        """
        pass
    
    def add_error(self, error: str) -> None:
        """添加错误信息"""
        self.errors.append(error)
