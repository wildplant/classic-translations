#!/usr/bin/env python3
"""
build.py — 经典神学与哲学重译项目构建脚本 (零第三方依赖)

功能：
1. 读取 articles/*/data.json 结构化三栏文稿与考据数据
2. 自动生成每篇独立的单文件三栏对照研读本 dist/<slug>.html
3. 自动导出每篇纯净版新译 Markdown (articles/<id>/new-zh.md)、旧译归档 (old-zh.md) 与英文原稿 (en.md)
4. 自动生成书目总览主页 dist/index.html

用法：
    python3 build.py
"""

import html
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = ROOT_DIR / "articles"
TEMPLATES_DIR = ROOT_DIR / "templates"
DIST_DIR = ROOT_DIR / "dist"


def render_fn_html(text: str) -> str:
    """将 [fn:N] 转换为交互式注释角标 HTML。"""
    return re.sub(
        r"\[fn:(\d+)\]",
        r'<sup class="fn-ref" data-fn="\1" role="button" tabindex="0" title="点击查看注[\1]">[\1]</sup>',
        text,
    )


def render_cell_blocks(raw_text: str) -> str:
    """将段落文本按双换行拆分为 <p> 或 <blockquote> 块，并渲染注释角标。"""
    blocks = [b.strip() for b in raw_text.strip().split("\n\n") if b.strip()]
    out = []
    for b in blocks:
        b_html = render_fn_html(b)
        if b_html.startswith("<blockquote"):
            out.append(b_html)
        else:
            out.append(f"<p>{b_html}</p>")
    return "\n".join(out)


def plain_preview(raw_text: str, length: int = 19) -> str:
    """提取去除标签与角标后的纯文本摘要，用于段落快速跳转菜单。"""
    txt = re.sub(r"\[fn:\d+\]", "", raw_text)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:length] + ("..." if len(txt) > length else "")


def to_markdown_text(raw_text: str) -> str:
    """将内部段落格式转换为干净的 Markdown 文本（含 [^N] 脚注与 > 引用块）。"""
    blocks = [b.strip() for b in raw_text.strip().split("\n\n") if b.strip()]
    md_blocks = []
    for b in blocks:
        b = re.sub(r"\[fn:(\d+)\]", r"[^\1]", b)
        b = re.sub(r"</?(?:i|em)>", "*", b)
        b = re.sub(r"</?(?:b|strong)>", "**", b)
        if b.startswith("<blockquote"):
            inner = re.sub(r"</?blockquote>", "", b).strip()
            inner = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n>\n> ", inner)
            inner = re.sub(r"<br\s*/?>", "\n> ", inner)
            md_blocks.append("> " + inner)
        else:
            md_blocks.append(b)
    return "\n\n".join(md_blocks)


def export_markdown_files(article_dir: Path, data: dict) -> None:
    """导出纯净版新译 new-zh.md、旧译归档 old-zh.md 与英文原稿 en.md。"""
    footnotes = data.get("footnotes", {})

    # 1. 导出 2026 精研新译 Markdown (new-zh.md)
    new_lines = [
        f"# {data['title_new_zh']}（{data['title_en']}）",
        "",
        f"- **作者**：{data['author_zh']}（{data['author']}）",
        f"- **年份与背景**：{data['occasion']}",
        f"- **原书篇序**：《荣耀之重：暨其他演讲》{data.get('book_chapter', '')}（旧译篇名：《{data['title_old_zh']}》）",
        "- **译本说明**：2026 精研新译本（圣经引文统一采用中文和合本［神版］）",
        "",
        "---",
        "",
    ]

    for p in data["paragraphs"]:
        if p.get("section_title"):
            new_lines.append(f"## {p['section_title']}")
            new_lines.append("")
        new_lines.append(to_markdown_text(p["new_zh"]))
        new_lines.append("")

    if footnotes:
        new_lines.extend(["---", "", "## 文献与历史考注", ""])
        for fn_id in sorted(footnotes.keys(), key=lambda x: int(x)):
            new_lines.append(f"[^{fn_id}]: {footnotes[fn_id]}")
            new_lines.append("")

    (article_dir / "new-zh.md").write_text("\n".join(new_lines), encoding="utf-8")

    # 2. 导出原书旧译归档 Markdown (old-zh.md)
    old_lines = [
        f"# {data['title_old_zh']}（{data['title_en']}）",
        "",
        f"- **作者**：{data['author_zh']}（{data['author']}）",
        f"- **译者**：{data['old_translator']}（{data['old_source']}）",
        "",
        "---",
        "",
    ]

    for p in data["paragraphs"]:
        if p.get("section_title"):
            old_lines.append(f"## {p['section_title']}")
            old_lines.append("")
        old_lines.append(to_markdown_text(p["old_zh"]))
        old_lines.append("")

    if footnotes:
        old_lines.extend(["---", "", "## 原书注释", ""])
        for fn_id in sorted(footnotes.keys(), key=lambda x: int(x)):
            old_lines.append(f"[^{fn_id}]: {footnotes[fn_id]}")
            old_lines.append("")

    (article_dir / "old-zh.md").write_text("\n".join(old_lines), encoding="utf-8")

    # 3. 导出英文原稿 Markdown (en.md)
    en_lines = [
        f"# {data['title_en']}",
        "",
        f"- **Author**: {data['author']}（{data['author_zh']}）",
        f"- **Year & Occasion**: {data['year']} · {data['occasion']}",
        f"- **Book Chapter**: 《荣耀之重：暨其他演讲》{data.get('book_chapter', '')}（新译《{data['title_new_zh']}》 / 旧译《{data['title_old_zh']}》）",
        f"- **Source**: {data.get('en_source', 'Original Text')}",
        "",
        "---",
        "",
    ]

    for p in data["paragraphs"]:
        sec = p.get("section_title_en") or p.get("section_title")
        if sec:
            en_lines.append(f"## {sec}")
            en_lines.append("")
        en_lines.append(to_markdown_text(p["en"]))
        en_lines.append("")

    (article_dir / "en.md").write_text("\n".join(en_lines), encoding="utf-8")

    # 同步输出到 dist/ 供静态网页直接访问和下载
    dist_article_dir = DIST_DIR / "articles" / data["id"]
    dist_article_dir.mkdir(parents=True, exist_ok=True)
    (dist_article_dir / "new-zh.md").write_text("\n".join(new_lines), encoding="utf-8")
    (dist_article_dir / "old-zh.md").write_text("\n".join(old_lines), encoding="utf-8")
    (dist_article_dir / "en.md").write_text("\n".join(en_lines), encoding="utf-8")


ZH_TO_ROMAN = {
    "第一篇": "PART I",
    "第二篇": "PART II",
    "第三篇": "PART III",
    "第四篇": "PART IV",
    "第五篇": "PART V",
    "第六篇": "PART VI",
    "第七篇": "PART VII",
    "第八篇": "PART VIII",
    "第九篇": "PART IX",
}


def build_article_html(reader_tpl: str, data: dict) -> str:
    """根据模板与单篇 data.json 渲染独立的单文件三栏对照 HTML。"""
    # 1. 段落跳转选项與三栏行
    para_options = []
    para_rows = []
    for p in data["paragraphs"]:
        num = p["num"]
        num_pad = f"{num:02d}"
        preview = html.escape(plain_preview(p["new_zh"]))
        para_options.append(
            f'<option value="row-{num}">第 {num_pad} 段：{preview}</option>'
        )

        if p.get("section_title"):
            banner = html.escape(p["section_title"])
            if p.get("section_title_en"):
                banner += f' <span style="font-weight:400;opacity:0.75;margin-left:8px;font-size:0.9em;">/ {html.escape(p["section_title_en"])}</span>'
            para_rows.append(
                f'<div class="section-banner-row">{banner}</div>'
            )

        en_html = render_cell_blocks(p["en"])
        old_html = render_cell_blocks(p["old_zh"])
        new_html = render_cell_blocks(p["new_zh"])

        row_block = f"""<article class="compare-row" data-row="{num}" id="row-{num}">
<!-- English -->
<div class="compare-cell cell-en col-en-cell">
<span class="row-badge">§ {num_pad}</span>
{en_html}
</div>
<!-- Old Translation -->
<div class="compare-cell cell-old col-old-cell">
<span class="row-badge">§ {num_pad}</span>
{old_html}
</div>
<!-- New Translation -->
<div class="compare-cell cell-new col-new-cell">
<span class="row-badge">§ {num_pad}</span>
{new_html}
</div>
</article>"""
        para_rows.append(row_block)

    # 2. 对勘卡片
    critique_items = []
    for c in data.get("critiques", []):
        critique_items.append(
            f"""<div class="critique-item">
<div class="critique-item-header">
<span class="critique-term">{html.escape(c['term'])}</span>
<span class="critique-loc">{html.escape(c['loc'])}</span>
</div>
<div class="critique-en">{html.escape(c['en'])}</div>
<div style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 4px;"><strong>旧译：</strong>{html.escape(c['old_zh'])}</div>
<div class="critique-diff">{html.escape(c['diff'])}</div>
</div>"""
        )

    # 3. 抽屉注释列表
    footnotes = data.get("footnotes", {})
    drawer_items = []
    for fn_id in sorted(footnotes.keys(), key=lambda x: int(x)):
        drawer_items.append(
            f"""<div class="drawer-fn-item" id="drawer-fn-{fn_id}">
<div class="drawer-fn-num">注 [{fn_id}]</div>
<div class="drawer-fn-content">{html.escape(footnotes[fn_id])}</div>
</div>"""
        )

    replacements = {
        "{{PAGE_TITLE}}": f"{data['author_zh']}《{data['title_new_zh']}》（{data['title_en']}）三栏逐段对照研读本",
        "{{TITLE_EN_UPPER}}": data["title_en"].upper(),
        "{{TITLE_EN}}": data["title_en"],
        "{{TITLE_NEW_ZH}}": data["title_new_zh"],
        "{{TITLE_OLD_ZH}}": data["title_old_zh"],
        "{{AUTHOR}}": data["author"],
        "{{OCCASION}}": data["occasion"],
        "{{YEAR}}": data["year"],
        "{{OLD_TRANSLATOR}}": data["old_translator"],
        "{{OLD_YEAR}}": data["old_year"],
        "{{OLD_SOURCE}}": data["old_source"],
        "{{EN_SOURCE}}": data["en_source"],
        "{{CRITIQUE_COUNT}}": str(len(data.get("critiques", []))),
        "{{FOOTNOTE_COUNT}}": str(len(footnotes)),
        "{{PARA_COUNT_PAD}}": f"{len(data['paragraphs']):02d}",
        "{{PARA_OPTIONS_HTML}}": "\n".join(para_options),
        "{{CRITIQUES_HTML}}": "\n\n".join(critique_items),
        "{{PARAGRAPHS_HTML}}": "\n".join(para_rows),
        "{{FOOTNOTES_DRAWER_HTML}}": "\n".join(drawer_items),
        "{{FOOTNOTES_JSON}}": json.dumps(footnotes, ensure_ascii=False),
    }

    out_html = reader_tpl
    for k, v in replacements.items():
        out_html = out_html.replace(k, v)
    return out_html


def build_index_html(index_tpl: str, articles: list[dict]) -> str:
    """生成书目总览主页 dist/index.html。"""
    entries = []
    for data in articles:
        crit_terms = " · ".join(c["term"].split("/")[0].strip() for c in data.get("critiques", [])[:4])
        chapter_str = data.get("book_chapter", "")
        roman_chapter = ZH_TO_ROMAN.get(chapter_str, "PART")
        entries.append(
            f"""<article class="article-entry">
    <div class="entry-sidebar">
        <div>
            <div class="chapter-roman">{roman_chapter}</div>
            <div class="chapter-sub">《荣耀之重》{html.escape(chapter_str)}</div>
        </div>
        <div class="year-mark">Anno {html.escape(data['year'])}</div>
    </div>
    <div class="entry-content">
        <div class="title-row">
            <h2 class="main-title">{html.escape(data['title_new_zh'])}</h2>
            <span class="old-title">旧译：《{html.escape(data['title_old_zh'])}》</span>
        </div>
        <div class="english-title">{html.escape(data['title_en'].upper())} — {html.escape(data['author'].upper())}</div>
        <p class="occasion-desc">{html.escape(data['occasion'])}。核心对勘词条：{html.escape(crit_terms)} 等。</p>
        <div class="meta-specs">
            <span>{len(data['paragraphs'])} 个自然段逐段对齐</span>
            <span class="dot">/</span>
            <span>{len(data.get('critiques', []))} 处核心对勘导读</span>
            <span class="dot">/</span>
            <span>{len(data.get('footnotes', {}))} 条文献与思想史考注</span>
        </div>
        <div class="entry-actions">
            <a class="btn-read-primary" href="{data['slug']}.html">进入三栏精研对照本 →</a>
            <a class="btn-link-sec" href="articles/{data['id']}/new-zh.md">查看 2026 纯净新译 (.md)</a>
        </div>
    </div>
</article>"""
        )

    out = index_tpl.replace("{{ARTICLE_COUNT}}", str(len(articles)))
    out = out.replace("{{CARDS_HTML}}", "\n".join(entries))
    return out


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    reader_tpl = (TEMPLATES_DIR / "reader.html").read_text(encoding="utf-8")
    index_tpl = (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")

    articles_data = []
    for data_file in sorted(ARTICLES_DIR.glob("*/data.json")):
        article_dir = data_file.parent
        data = json.loads(data_file.read_text(encoding="utf-8"))
        articles_data.append(data)

        # 导出 Markdown 文稿
        export_markdown_files(article_dir, data)

        # 构建单文件三栏研读 HTML
        html_out = build_article_html(reader_tpl, data)
        out_path = DIST_DIR / f"{data['slug']}.html"
        out_path.write_text(html_out, encoding="utf-8")
        print(
            f"[OK] Built {out_path.relative_to(ROOT_DIR)} "
            f"({len(data['paragraphs'])} paras, {len(data.get('critiques', []))} critiques, {len(data.get('footnotes', {}))} footnotes)"
        )

    articles_data.sort(key=lambda d: d.get("order", 999))
    index_out = build_index_html(index_tpl, articles_data)
    index_path = DIST_DIR / "index.html"
    index_path.write_text(index_out, encoding="utf-8")
    print(f"[OK] Built {index_path.relative_to(ROOT_DIR)} ({len(articles_data)} articles indexed)")


if __name__ == "__main__":
    main()
