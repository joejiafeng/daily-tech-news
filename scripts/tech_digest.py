#!/usr/bin/env python3
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import feedparser
import pytz
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from siliconflow_client import messages_create

# 加载 .env 文件（如果存在）
load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def to_iso(ts: Optional[int], tz: pytz.BaseTzInfo) -> Optional[str]:
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=tz).isoformat()


def clean_text(text: str) -> str:
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text(" ", strip=True)
    return " ".join(cleaned.split())


def trim_text(text: str, limit: int = 180) -> str:
    cleaned = clean_text(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def fetch_json(url: str, timeout: int = 20) -> Any:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def fetch_v2ex(config: Dict[str, Any], tz: pytz.BaseTzInfo) -> List[Dict[str, Any]]:
    url = config["sources"]["v2ex"]["url"]
    limit = config["sources"]["v2ex"]["limit"]
    data = fetch_json(url)
    items = []
    for entry in data[:limit]:
        items.append(
            {
                "source": "V2EX",
                "source_type": "v2ex",
                "title": entry.get("title", "").strip(),
                "url": entry.get("url", "").strip(),
                "summary": trim_text(entry.get("content", "")),
                "published": to_iso(entry.get("created"), tz),
                "score": entry.get("replies", 0),
            }
        )
    return items


def fetch_hackernews(config: Dict[str, Any], tz: pytz.BaseTzInfo) -> List[Dict[str, Any]]:
    top_url = config["sources"]["hackernews"]["topstories_url"]
    item_url = config["sources"]["hackernews"]["item_url"]
    limit = config["sources"]["hackernews"]["limit"]
    ids = fetch_json(top_url)
    items = []
    for story_id in ids[:limit]:
        story = fetch_json(item_url.format(id=story_id))
        if story.get("type") != "story":
            continue
        items.append(
            {
                "source": "Hacker News",
                "source_type": "hackernews",
                "title": story.get("title", "").strip(),
                "url": story.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
                "summary": trim_text(story.get("text", "")),
                "published": to_iso(story.get("time"), tz),
                "score": story.get("score", 0),
            }
        )
        if len(items) >= limit:
            break
    return items


def fetch_rss(config: Dict[str, Any], tz: pytz.BaseTzInfo) -> List[Dict[str, Any]]:
    rss_config = config["sources"]["rss"]
    limit_total = rss_config["limit_total"]
    feeds = rss_config["feeds"]
    items: List[Dict[str, Any]] = []

    for feed in feeds:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries:
            published_ts = None
            if entry.get("published_parsed"):
                published_ts = int(time.mktime(entry.published_parsed))
            elif entry.get("updated_parsed"):
                published_ts = int(time.mktime(entry.updated_parsed))

            summary = entry.get("summary") or entry.get("description") or ""
            items.append(
                {
                    "source": feed["name"],
                    "source_type": "rss",
                    "category": feed.get("category"),
                    "title": str(entry.get("title", "")).strip(),
                    "url": str(entry.get("link", "")).strip(),
                    "summary": trim_text(summary),
                    "published": to_iso(published_ts, tz),
                }
            )
            if len(items) >= limit_total:
                return items
    return items


def build_prompt(
    date_str: str,
    v2ex_items: List[Dict[str, Any]],
    hn_items: List[Dict[str, Any]],
    rss_items: List[Dict[str, Any]],
    digest_cfg: Dict[str, Any],
) -> str:
    min_items = digest_cfg["min_items_per_section"]
    max_items = digest_cfg["max_items_per_section"]
    sections = [
        "1. 今日热点",
        "2. 技术趋势",
        "3. 产品观察",
        "4. 推荐阅读",
    ]

    def format_items(items: List[Dict[str, Any]]) -> str:
        lines = []
        for it in items:
            title = it.get("title", "")
            url = it.get("url", "")
            summary = it.get("summary", "")
            source = it.get("source", "")
            lines.append(f"- {title} ({source}) {url} | {summary}")
        return "\n".join(lines)

    payload = [
        "请根据以下素材生成今日中文科技简报，必须严格输出 Markdown。",
        "",
        f"日期：{date_str}",
        "",
        "输出格式要求：",
        f"- 标题行：# Daily Tech News | {date_str}",
        "- 先给 1 段导语（2-3 句）",
        "- 接着输出 4 个二级标题段落，标题必须与下面一致：",
        *[f"  - ## {s}" for s in sections],
        f"- 每个段落包含 {min_items}-{max_items} 条要点，用无序列表",
        "- 每条要点格式：",
        "  - [标题文字](URL) (来源)",
        "    200字以内的内容总结，说明该新闻的核心要点、影响或意义（不需要加 bullet point，也不要加'总结：'前缀，直接另起一行缩进）",
        "- 示例格式：",
        "  - [量旋科技完成数亿元 C 轮融资](https://example.com) (36kr)",
        "    量旋科技是一家专注于量子计算商业化的公司，此次 C 轮融资数亿元，显示了资本市场对量子计算技术的持续看好。公司由清华和哈佛背景的团队创立，致力于推动量子计算从实验室走向实际应用。",
        "- 链接必须是可点击的 Markdown 格式，不能是纯文本 URL",
        "- 总结必须基于下方素材中的信息，严禁编造不存在的新闻或信息",
        "",
        "素材如下：",
        "",
        "V2EX 热门：",
        format_items(v2ex_items),
        "",
        "Hacker News Top：",
        format_items(hn_items),
        "",
        "科技媒体 RSS：",
        format_items(rss_items),
    ]
    return "\n".join(payload)


def save_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def convert_urls_to_links(text: str) -> str:
    """
    将 Markdown 中的纯文本 URL 转换为 Markdown 链接格式。
    匹配格式：- 文本 (来源) https://url -> - [文本](https://url) (来源)
    """
    import re
    
    lines = text.split('\n')
    result_lines = []
    
    for line in lines:
        # 匹配列表项格式：- 文本 (来源) URL
        # 例如：- 量旋科技完成数亿元 C 轮融资 (36kr) https://36kr.com/...
        pattern = r'^(\s*-\s+)(.+?)\s+\(([^)]+)\)\s+(https?://[^\s\)]+)(.*)$'
        match = re.match(pattern, line)
        
        if match:
            indent = match.group(1)  # "- " 或 "  - "
            text_part = match.group(2).strip()
            source = match.group(3).strip()
            url = match.group(4).strip()
            rest = match.group(5).strip()
            
            # 如果已经是链接格式，跳过
            if '[' in text_part and '](' in text_part:
                result_lines.append(line)
            else:
                # 转换为 Markdown 链接格式
                new_line = f"{indent}[{text_part}]({url}) ({source})"
                if rest:
                    new_line += f" {rest}"
                result_lines.append(new_line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)


def save_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")


def main() -> None:
    config = load_config()
    tz = pytz.timezone(config["output"]["timezone"])
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")

    output_dir = PROJECT_ROOT / config["output"]["output_dir"]
    ensure_output_dir(output_dir)

    v2ex_items = fetch_v2ex(config, tz)
    hn_items = fetch_hackernews(config, tz)
    rss_items = fetch_rss(config, tz)

    sources_payload = {
        "date": date_str,
        "generated_at": now.isoformat(),
        "v2ex": v2ex_items,
        "hackernews": hn_items,
        "rss": rss_items,
    }
    save_json(output_dir / f"{date_str}.sources.json", sources_payload)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL") or config["llm"]["base_url"]
    if not api_key:
        print("错误: 请设置 ANTHROPIC_API_KEY 环境变量")
        sys.exit(1)

    system_prompt = "你是资深科技编辑，擅长将多源科技新闻整理为高质量中文简报。"
    user_prompt = build_prompt(
        date_str,
        v2ex_items,
        hn_items,
        rss_items,
        config["digest"],
    )

    digest_markdown = messages_create(
        api_key=api_key,
        base_url=base_url,
        model=config["llm"]["model"],
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=config["llm"]["max_tokens"],
        temperature=config["llm"]["temperature"],
        top_p=config["llm"]["top_p"],
        top_k=config["llm"]["top_k"],
    )

    # 将纯文本 URL 转换为 Markdown 链接格式
    digest_markdown = convert_urls_to_links(digest_markdown)
    
    dated_path = output_dir / f"{date_str}.md"
    latest_path = output_dir / "latest.md"
    save_text(dated_path, digest_markdown)
    save_text(latest_path, digest_markdown)

    print(f"已生成: {dated_path}")
    print(f"已更新: {latest_path}")


if __name__ == "__main__":
    main()
