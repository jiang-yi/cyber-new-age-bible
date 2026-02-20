#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT / "流转纪·容量篇.md"
OUT_DIR = ROOT / "translations"

LANGUAGES = [
    ("el", "Greek", "The Rhythms of Flow and Capacity (Greek Edition)"),
    ("la", "Latin", "The Rhythms of Flow and Capacity (Latin Edition)"),
    ("ja", "Japanese", "The Rhythms of Flow and Capacity (Japanese Edition)"),
    ("zh-Hans", "Chinese (Simplified)", "流转纪·容量篇（简体中文版）"),
    ("ko", "Korean", "The Rhythms of Flow and Capacity (Korean Edition)"),
    ("es", "Spanish", "The Rhythms of Flow and Capacity (Spanish Edition)"),
    ("zh-Hant", "Chinese (Traditional)", "流轉紀·容量篇（繁體中文版）"),
    ("hi", "Hindi", "The Rhythms of Flow and Capacity (Hindi Edition)"),
    ("ar", "Standard Arabic", "The Rhythms of Flow and Capacity (Arabic Edition)"),
    ("fr", "French", "The Rhythms of Flow and Capacity (French Edition)"),
    ("bn", "Bengali", "The Rhythms of Flow and Capacity (Bengali Edition)"),
    ("pt", "Portuguese", "The Rhythms of Flow and Capacity (Portuguese Edition)"),
    ("ru", "Russian", "The Rhythms of Flow and Capacity (Russian Edition)"),
    ("id", "Indonesian", "The Rhythms of Flow and Capacity (Indonesian Edition)"),
    ("he", "Hebrew", "The Rhythms of Flow and Capacity (Hebrew Edition)"),
    ("de", "German", "The Rhythms of Flow and Capacity (German Edition)"),
    ("it", "Italian", "The Rhythms of Flow and Capacity (Italian Edition)"),
    ("pl", "Polish", "The Rhythms of Flow and Capacity (Polish Edition)"),
    ("nl", "Dutch", "The Rhythms of Flow and Capacity (Dutch Edition)"),
    ("sv", "Scandinavian (Swedish)", "The Rhythms of Flow and Capacity (Scandinavian/Swedish Edition)"),
    ("cs", "Czech", "The Rhythms of Flow and Capacity (Czech Edition)"),
    ("hu", "Hungarian", "The Rhythms of Flow and Capacity (Hungarian Edition)"),
    ("uk", "Ukrainian", "The Rhythms of Flow and Capacity (Ukrainian Edition)"),
    ("tr", "Turkish", "The Rhythms of Flow and Capacity (Turkish Edition)"),
]


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
        "> This file is generated from the standalone volume in this repository.\n"
        "> The body below remains source text until a full human-reviewed translation pass is completed.\n\n"
    )
    return header + source_text


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_text = SOURCE_PATH.read_text(encoding="utf-8")

    for code, lang_name, title in LANGUAGES:
        out_path = OUT_DIR / f"The_Rhythms_of_Flow_and_Capacity_{code}.md"
        text = to_traditional_chinese(source_text) if code == "zh-Hant" else source_text
        out_path.write_text(build_document(title, lang_name, text), encoding="utf-8")


if __name__ == "__main__":
    main()
