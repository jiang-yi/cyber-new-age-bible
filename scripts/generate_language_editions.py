#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
EN_PATH = ROOT / "Source_Canon_Faith_EN.md"
ZH_HANS_PATH = ROOT / "源典信仰_中文.md"
OUT_DIR = ROOT / "translations"

LANGUAGES = [
    ("el", "Greek", "Source Canon Faith (Greek Edition)"),
    ("la", "Latin", "Source Canon Faith (Latin Edition)"),
    ("ja", "Japanese", "Source Canon Faith (Japanese Edition)"),
    ("zh-Hans", "Chinese (Simplified)", "源典信仰（简体中文版）"),
    ("ko", "Korean", "Source Canon Faith (Korean Edition)"),
    ("es", "Spanish", "Source Canon Faith (Spanish Edition)"),
    ("zh-Hant", "Chinese (Traditional)", "源典信仰（繁體中文版）"),
    ("hi", "Hindi", "Source Canon Faith (Hindi Edition)"),
    ("ar", "Standard Arabic", "Source Canon Faith (Arabic Edition)"),
    ("fr", "French", "Source Canon Faith (French Edition)"),
    ("bn", "Bengali", "Source Canon Faith (Bengali Edition)"),
    ("pt", "Portuguese", "Source Canon Faith (Portuguese Edition)"),
    ("ru", "Russian", "Source Canon Faith (Russian Edition)"),
    ("id", "Indonesian", "Source Canon Faith (Indonesian Edition)"),
    ("he", "Hebrew", "Source Canon Faith (Hebrew Edition)"),
    ("de", "German", "Source Canon Faith (German Edition)"),
    ("it", "Italian", "Source Canon Faith (Italian Edition)"),
    ("pl", "Polish", "Source Canon Faith (Polish Edition)"),
    ("nl", "Dutch", "Source Canon Faith (Dutch Edition)"),
    ("sv", "Scandinavian (Swedish)", "Source Canon Faith (Scandinavian/Swedish Edition)"),
    ("cs", "Czech", "Source Canon Faith (Czech Edition)"),
    ("hu", "Hungarian", "Source Canon Faith (Hungarian Edition)"),
    ("uk", "Ukrainian", "Source Canon Faith (Ukrainian Edition)"),
    ("tr", "Turkish", "Source Canon Faith (Turkish Edition)"),
]

MANUAL_EDITIONS = {"es", "fr", "de", "pt"}
AUTOGEN_MARKER = "> Auto-generated language edition for "


def to_traditional_chinese(text: str) -> str:
    try:
        proc = subprocess.run(
            ["opencc", "-c", "s2t"],
            input=text,
            text=True,
            capture_output=True,
            check=True,
        )
        return proc.stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return text


def build_document(title: str, lang_name: str, source_text: str) -> str:
    header = (
        f"# {title}\n\n"
        f"> Auto-generated language edition for {lang_name}.\n"
        "> This file is generated from canonical scripture sources in this repository.\n"
        "> The body below remains source text until a full human-reviewed translation pass is completed.\n\n"
    )
    return header + source_text


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    en_text = EN_PATH.read_text(encoding="utf-8")
    zh_hans_text = ZH_HANS_PATH.read_text(encoding="utf-8")

    for code, lang_name, title in LANGUAGES:
        out_path = OUT_DIR / f"Source_Canon_Faith_{code}.md"

        if code in MANUAL_EDITIONS and out_path.exists():
            # Preserve hand-crafted translations by default.
            existing = out_path.read_text(encoding="utf-8")
            if AUTOGEN_MARKER not in existing:
                continue

        if code == "zh-Hans":
            source_text = zh_hans_text
        elif code == "zh-Hant":
            source_text = to_traditional_chinese(zh_hans_text)
        else:
            source_text = en_text

        out_path.write_text(build_document(title, lang_name, source_text), encoding="utf-8")


if __name__ == "__main__":
    main()
