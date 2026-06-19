from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://milano-sports.com"
SAMPLE_KEYWORD = "米兰体育app"


@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    description: str
    tags: List[str]
    created_at: Optional[str] = None
    priority: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        return f"[{self.keyword}] from {self.source_url} — {self.description[:50]}..."

    def tag_line(self) -> str:
        return ", ".join(self.tags) if self.tags else "无标签"


@dataclass
class KeywordCollection:
    notes: List[KeywordNote]

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sort_by_priority(self, reverse: bool = True) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda n: n.priority, reverse=reverse)

    def render_report(self) -> str:
        lines = ["=== 关键词笔记报告 ==="]
        for i, note in enumerate(self.notes, 1):
            lines.append(
                f"{i}. {note.keyword}\n"
                f"   来源: {note.source_url}\n"
                f"   描述: {note.description}\n"
                f"   标签: {note.tag_line()}\n"
                f"   优先级: {note.priority}\n"
                f"   创建时间: {note.created_at}\n"
            )
        return "\n".join(lines)


def format_keyword_output(notes: List[KeywordNote], style: str = "plain") -> str:
    if style == "plain":
        return "\n".join(f"{n.keyword} | {n.source_url}" for n in notes)
    elif style == "detailed":
        return "\n---\n".join(
            f"关键词: {n.keyword}\nURL: {n.source_url}\n描述: {n.description}"
            for n in notes
        )
    elif style == "compact":
        return " | ".join(f"{n.keyword}({n.priority})" for n in notes)
    else:
        raise ValueError(f"未知样式: {style}")


def build_sample_notes() -> KeywordCollection:
    notes = [
        KeywordNote(
            keyword=SAMPLE_KEYWORD,
            source_url=SAMPLE_URL,
            description="米兰体育官方应用，提供体育新闻与赛事服务。",
            tags=["体育", "应用", "米兰"],
            priority=5,
        ),
        KeywordNote(
            keyword="AC米兰新闻",
            source_url="https://milano-sports.com/news",
            description="最新AC米兰俱乐部动态与赛程。",
            tags=["足球", "AC米兰"],
            priority=3,
        ),
        KeywordNote(
            keyword="意甲积分榜",
            source_url="https://milano-sports.com/standings",
            description="意甲联赛实时排名数据。",
            tags=["意甲", "数据"],
            priority=2,
        ),
    ]
    return KeywordCollection(notes=notes)


def demo_usage() -> None:
    collection = build_sample_notes()
    print(collection.render_report())

    print("--- 按优先级排序 ---")
    for note in collection.sort_by_priority():
        print(note.summary())

    print("\n--- 标签过滤: 体育 ---")
    for note in collection.filter_by_tag("体育"):
        print(f"  -> {note.keyword}")

    print("\n--- 紧凑样式输出 ---")
    print(format_keyword_output(collection.notes, style="compact"))


if __name__ == "__main__":
    demo_usage()