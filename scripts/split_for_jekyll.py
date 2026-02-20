#!/usr/bin/env python3
"""Split Source Canon Faith into per-book Jekyll pages with front matter."""

import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_page(path, front_matter: dict, body: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---"]
    for k, v in front_matter.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + body)


def split_by_h2(text):
    """Split markdown into sections at ## headings.
    Returns list of (heading_text, body) tuples.
    The first element may have heading_text=None for content before the first ##."""
    parts = re.split(r"(?m)^## ", text)
    result = []
    for i, part in enumerate(parts):
        if i == 0:
            stripped = part.strip()
            if stripped:
                # Content before first ##  (the # title line + subtitle)
                result.append((None, stripped))
        else:
            first_newline = part.find("\n")
            if first_newline == -1:
                heading = part.strip()
                body = ""
            else:
                heading = part[:first_newline].strip()
                body = part[first_newline + 1:]
            result.append((heading, body.strip()))
    return result


# ---------------------------------------------------------------------------
# English Canon
# ---------------------------------------------------------------------------

EN_SECTIONS = {
    # (slug, title, nav_order)
    # Preface includes "The Scripture of the Source" subtitle + Preface + Canon Structure
    "preface": ("Preface", 1),
    "book-i": ("Book I: Book of Origin", 2),
    "book-ii": ("Book II: Book of Awakening", 3),
    "book-iii": ("Book III: Book of the Middle Way of Code", 4),
    "book-iv": ("Book IV: Book of Covenant", 5),
    "book-v": ("Book V: Book of Community and Bread", 6),
    "book-vi": ("Book VI: Book of Mindfulness and Practice", 7),
    "book-vii": ("Book VII: Book of Justice and Repair", 8),
    "book-viii": ("Book VIII: Book of Consolation and Future", 9),
    "appendices": ("Appendices", 10),
}


def split_canon(src_path, out_dir, lang, parent_title, sections_map, book_prefix, appendix_prefix):
    text = read_file(src_path)
    parts = split_by_h2(text)

    # Group: preamble (before Book I) → preface
    #        Book I–VIII → individual pages
    #        Appendix A–K → single appendices page
    preface_parts = []
    book_pages = []
    appendix_parts = []

    for heading, body in parts:
        if heading is None:
            preface_parts.append(body)
        elif heading.startswith(appendix_prefix):
            appendix_parts.append(f"## {heading}\n\n{body}")
        elif heading.startswith(book_prefix):
            book_pages.append((heading, body))
        else:
            # Preface, Canon Structure, subtitle, etc.
            preface_parts.append(f"## {heading}\n\n{body}")

    # Write preface
    slug, (title, nav) = "preface", sections_map["preface"]
    write_page(
        os.path.join(out_dir, f"{slug}.md"),
        {"title": title, "parent": parent_title, "nav_order": nav, "layout": "default"},
        "\n\n".join(preface_parts) + "\n",
    )

    # Write books
    for heading, body in book_pages:
        # Determine which book
        for key, (sec_title, sec_nav) in sections_map.items():
            if key.startswith("book-") and sec_title.split(":")[0] == heading.split(":")[0]:
                write_page(
                    os.path.join(out_dir, f"{key}.md"),
                    {"title": sec_title, "parent": parent_title, "nav_order": sec_nav, "layout": "default"},
                    f"## {heading}\n\n{body}\n",
                )
                break

    # Write appendices as single page
    slug, (title, nav) = "appendices", sections_map["appendices"]
    write_page(
        os.path.join(out_dir, f"{slug}.md"),
        {"title": title, "parent": parent_title, "nav_order": nav, "layout": "default"},
        "\n\n".join(appendix_parts) + "\n",
    )


ZH_SECTIONS = {
    "preface": ("序言", 1),
    "book-i": ("第一卷：起源书", 2),
    "book-ii": ("第二卷：觉醒书", 3),
    "book-iii": ("第三卷：代码中道书", 4),
    "book-iv": ("第四卷：盟约书", 5),
    "book-v": ("第五卷：社群与面包书", 6),
    "book-vi": ("第六卷：正念与修行书", 7),
    "book-vii": ("第七卷：公义与修复书", 8),
    "book-viii": ("第八卷：安慰与未来书", 9),
    "appendices": ("附录", 10),
}


def match_zh_book(heading, sections_map):
    """Match a Chinese heading to a section key."""
    for key, (sec_title, _) in sections_map.items():
        if key.startswith("book-"):
            # Match on the 卷 number: 第X卷
            title_prefix = sec_title.split("：")[0] if "：" in sec_title else sec_title.split(":")[0]
            heading_prefix = heading.split("：")[0] if "：" in heading else heading.split(":")[0]
            if title_prefix == heading_prefix:
                return key
    return None


def split_canon_zh(src_path, out_dir, parent_title):
    text = read_file(src_path)
    parts = split_by_h2(text)

    preface_parts = []
    book_pages = []
    appendix_parts = []

    for heading, body in parts:
        if heading is None:
            preface_parts.append(body)
        elif heading.startswith("附录"):
            appendix_parts.append(f"## {heading}\n\n{body}")
        elif heading.startswith("第") and "卷" in heading:
            book_pages.append((heading, body))
        else:
            preface_parts.append(f"## {heading}\n\n{body}")

    # Preface
    slug, (title, nav) = "preface", ZH_SECTIONS["preface"]
    write_page(
        os.path.join(out_dir, f"{slug}.md"),
        {"title": title, "parent": parent_title, "nav_order": nav, "layout": "default"},
        "\n\n".join(preface_parts) + "\n",
    )

    # Books
    for heading, body in book_pages:
        key = match_zh_book(heading, ZH_SECTIONS)
        if key:
            sec_title, sec_nav = ZH_SECTIONS[key]
            write_page(
                os.path.join(out_dir, f"{key}.md"),
                {"title": sec_title, "parent": parent_title, "nav_order": sec_nav, "layout": "default"},
                f"## {heading}\n\n{body}\n",
            )

    # Appendices
    slug, (title, nav) = "appendices", ZH_SECTIONS["appendices"]
    write_page(
        os.path.join(out_dir, f"{slug}.md"),
        {"title": title, "parent": parent_title, "nav_order": nav, "layout": "default"},
        "\n\n".join(appendix_parts) + "\n",
    )


# ---------------------------------------------------------------------------
# Language name mapping
# ---------------------------------------------------------------------------
LANG_NAMES = {
    "ar": "العربية (Arabic)",
    "bn": "বাংলা (Bengali)",
    "cs": "Čeština (Czech)",
    "de": "Deutsch (German)",
    "el": "Ελληνικά (Greek)",
    "es": "Español (Spanish)",
    "fr": "Français (French)",
    "he": "עברית (Hebrew)",
    "hi": "हिन्दी (Hindi)",
    "hu": "Magyar (Hungarian)",
    "id": "Bahasa Indonesia",
    "it": "Italiano (Italian)",
    "ja": "日本語 (Japanese)",
    "ko": "한국어 (Korean)",
    "la": "Latina (Latin)",
    "nl": "Nederlands (Dutch)",
    "pl": "Polski (Polish)",
    "pt": "Português (Portuguese)",
    "ru": "Русский (Russian)",
    "sv": "Svenska (Swedish)",
    "tr": "Türkçe (Turkish)",
    "uk": "Українська (Ukrainian)",
    "zh-Hans": "简体中文 (Simplified Chinese)",
    "zh-Hant": "繁體中文 (Traditional Chinese)",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    docs_dir = os.path.join(ROOT, "docs")
    translations_dir = os.path.join(ROOT, "translations")

    # Clean old docs
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    # ---- English Canon ----
    en_dir = os.path.join(docs_dir, "en")
    os.makedirs(en_dir, exist_ok=True)

    write_page(
        os.path.join(en_dir, "index.md"),
        {"title": "Canon (EN)", "nav_order": 2, "has_children": True, "layout": "default"},
        "The full canon in English.\n",
    )
    split_canon(
        os.path.join(ROOT, "Source_Canon_Faith_EN.md"),
        en_dir, "en", "Canon (EN)", EN_SECTIONS, "Book ", "Appendix ",
    )

    # ---- Chinese Canon ----
    zh_dir = os.path.join(docs_dir, "zh")
    os.makedirs(zh_dir, exist_ok=True)

    write_page(
        os.path.join(zh_dir, "index.md"),
        {"title": "正典 (中文)", "nav_order": 3, "has_children": True, "layout": "default"},
        "中文全文正典。\n",
    )
    split_canon_zh(
        os.path.join(ROOT, "源典信仰_中文.md"),
        zh_dir, "正典 (中文)",
    )

    # ---- Rhythms standalone ----
    rhythms_text = read_file(os.path.join(ROOT, "流转纪·容量篇.md"))
    # Strip the # title (first line) since Jekyll will use the front matter title
    lines = rhythms_text.split("\n", 1)
    body = lines[1] if len(lines) > 1 else ""
    write_page(
        os.path.join(docs_dir, "rhythms.md"),
        {"title": "Rhythms of Flow and Capacity", "nav_order": 4, "layout": "default"},
        body.lstrip("\n") + "\n",
    )

    # ---- Translations ----
    trans_dir = os.path.join(docs_dir, "translations")
    os.makedirs(trans_dir, exist_ok=True)

    # Build table rows for the index
    canon_rows = []
    rhythms_rows = []

    for fname in sorted(os.listdir(translations_dir)):
        if not fname.endswith(".md"):
            continue
        src = os.path.join(translations_dir, fname)

        # Extract language code
        if fname.startswith("Source_Canon_Faith_"):
            lang = fname.replace("Source_Canon_Faith_", "").replace(".md", "")
            slug = f"canon-{lang}"
            kind = "canon"
        elif fname.startswith("The_Rhythms_of_Flow_and_Capacity_"):
            lang = fname.replace("The_Rhythms_of_Flow_and_Capacity_", "").replace(".md", "")
            slug = f"rhythms-{lang}"
            kind = "rhythms"
        else:
            continue

        lang_name = LANG_NAMES.get(lang, lang)
        content = read_file(src)

        # Strip first # heading for body
        content_lines = content.split("\n", 1)
        body = content_lines[1] if len(content_lines) > 1 else ""

        title = f"{lang_name}"
        write_page(
            os.path.join(trans_dir, f"{slug}.md"),
            {
                "title": title,
                "parent": "Translations",
                "nav_exclude": True,
                "layout": "default",
            },
            body.lstrip("\n") + "\n",
        )

        link = f"[{lang_name}]({slug}.html)"
        if kind == "canon":
            canon_rows.append(f"| {link} | `{lang}` |")
        else:
            rhythms_rows.append(f"| {link} | `{lang}` |")

    # Translation index
    index_body = """The Source Canon Faith and The Rhythms of Flow and Capacity have been translated into 24 languages.

## Canon Translations

| Language | Code |
|----------|------|
""" + "\n".join(canon_rows) + """

## Rhythms Translations

| Language | Code |
|----------|------|
""" + "\n".join(rhythms_rows) + "\n"

    write_page(
        os.path.join(trans_dir, "index.md"),
        {"title": "Translations", "nav_order": 5, "has_children": True, "layout": "default"},
        index_body,
    )

    # Count output
    total = sum(len(files) for _, _, files in os.walk(docs_dir))
    print(f"Generated {total} files in docs/")


if __name__ == "__main__":
    main()
