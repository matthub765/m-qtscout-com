import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class SiteEntry:
    """A structured representation of a site record with key metadata."""
    title: str
    url: str
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    description: str = ""

    def summary(self) -> str:
        tag_part = ", ".join(self.tags) if self.tags else "无标签"
        kw_part = ", ".join(self.keywords) if self.keywords else "无可关键词"
        return (
            f"站点：{self.title}\n"
            f"URL：{self.url}\n"
            f"标签：{tag_part}\n"
            f"关键词：{kw_part}\n"
            f"简介：{self.description}"
        )


class SiteSummaryGenerator:
    """Read built-in site data and output a structured summary."""

    def __init__(self, seed_data: Optional[dict] = None):
        self._entries: List[SiteEntry] = []
        if seed_data:
            self._load_from_dict(seed_data)
        else:
            self._load_default()

    def _load_from_dict(self, data: dict):
        raw = data.get("sites", [])
        for item in raw:
            entry = SiteEntry(
                title=item.get("name", "未命名"),
                url=item.get("link", ""),
                tags=item.get("tags", []),
                keywords=item.get("keywords", []),
                description=item.get("desc", "")
            )
            self._entries.append(entry)

    def _load_default(self):
        """Load internal example site data (no external requests)."""
        default_sites = [
            {
                "name": "球探情报站",
                "link": "https://m-qtscout.com",
                "tags": ["球探", "足球", "数据分析"],
                "keywords": ["球探", "比赛预测", "实时数据"],
                "desc": "提供足球比赛实时情报与深度数据分析，协助球迷洞察赛场趋势。"
            },
            {
                "name": "技术参考笔记",
                "link": "https://example.com/tech-notes",
                "tags": ["技术", "文档", "学习"],
                "keywords": ["Python", "数据结构", "算法"],
                "desc": "个人技术学习笔记，涵盖常见编程语言与算法实现。"
            }
        ]
        self._load_from_dict({"sites": default_sites})

    def add_entry(self, entry: SiteEntry):
        self._entries.append(entry)

    def remove_entry(self, index: int) -> bool:
        if 0 <= index < len(self._entries):
            self._entries.pop(index)
            return True
        return False

    def generate_text_report(self) -> str:
        if not self._entries:
            return "（暂无站点资料）"
        lines = ["========== 站点结构摘要 =========="]
        for i, entry in enumerate(self._entries, start=1):
            lines.append(f"\n--- 站点 {i} ---")
            lines.append(entry.summary())
        lines.append("\n========== 摘要结束 ==========")
        return "\n".join(lines)

    def to_json(self, indent: int = 2) -> str:
        dict_list = [asdict(e) for e in self._entries]
        return json.dumps(dict_list, ensure_ascii=False, indent=indent)

    def count(self) -> int:
        return len(self._entries)


def demonstrate():
    """Simple demonstration of the module's functionality."""
    gen = SiteSummaryGenerator()
    print(gen.generate_text_report())

    extra_site = SiteEntry(
        title="球探观察室",
        url="https://m-qtscout.com/observation",
        tags=["球探", "观察", "统计"],
        keywords=["球探", "战术分析", "球队数据"],
        description="聚焦赛事战术细节与球队数据变化，深度解读每场比赛。"
    )
    gen.add_entry(extra_site)
    print("\n--- 添加一条新站点后 ---")
    print(gen.generate_text_report())

    print("\n--- JSON 输出 ---")
    print(gen.to_json())


if __name__ == "__main__":
    demonstrate()