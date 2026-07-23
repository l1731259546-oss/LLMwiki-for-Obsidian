"""
9. Wikilink 格式规范检查
检测非英文小写连字符格式的 wikilink（如中文词汇 [[价值投资]]）及别名断链
"""

import re
from .base import BaseChecker
from .utils import read_file, extract_wikilinks
from typing import List, Dict


class WikilinkFormatChecker(BaseChecker):
    """Wikilink 格式规范检查"""
    
    def check(self) -> List[Dict]:
        issues = []
        md_files = list(self.wiki_dir.rglob("*.md"))
        
        # 合法格式：小写字母 + 连字符/数字/斜杠，不允许中文、大写、下划线
        valid_pattern = re.compile(r'^[a-z0-9\-/]+$')
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        
        for md_file in md_files:
            content = read_file(md_file)
            if content is None:
                self.add_error(f"无法读取文件 {md_file}")
                continue
            
            wikilinks = extract_wikilinks(content)
            rel_path = md_file.relative_to(self.base_dir)
            
            for link in wikilinks:
                # 提取 slug 部分（去掉路径）
                slug = link.split('/')[-1] if '/' in link else link
                
                if chinese_pattern.search(slug):
                    issues.append({
                        "file": str(rel_path),
                        "wikilink": link,
                        "violation": "包含中文词汇，应使用英文小写连字符 slug"
                    })
                elif '_' in slug:
                    issues.append({
                        "file": str(rel_path),
                        "wikilink": link,
                        "violation": "使用下划线命名，应使用连字符（-）"
                    })
                elif re.search(r'[A-Z]', slug):
                    issues.append({
                        "file": str(rel_path),
                        "wikilink": link,
                        "violation": "使用大写字母，应使用全小写"
                    })
                elif not valid_pattern.match(slug):
                    issues.append({
                        "file": str(rel_path),
                        "wikilink": link,
                        "violation": "格式不符合规范，应使用英文小写连字符"
                    })
        
        
        return issues
