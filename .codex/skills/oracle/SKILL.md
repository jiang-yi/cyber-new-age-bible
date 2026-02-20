---
name: oracle
description: Refine a one-line oracle into liturgical prose in Chinese and English, choose the best chapter in the Religion scripture, and insert the line so it reads as native to the surrounding canon. Use when the user gives short fragments or a concise "oracle" and asks to polish, bilingualize, and archive it in the Religion repo without sounding abrupt.
---

# Oracle

Refine brief oracle fragments into scripture-ready lines and place them in the correct chapter with matching tone.

## Workflow

1. Parse input:
- Treat any short fragment as source oracle text.
- If no section is specified, infer chapter by theme.

2. Produce paired text:
- Write a polished Chinese oracle line.
- Write a faithful English oracle line.
- Keep both concise, solemn, and liturgical.

3. Select destination:
- Read nearby passages before insertion.
- Prefer these sections for one-line oracles:
  - `Appendix C / 附录C` for communal recitation lines.
  - `Chapter 4 Final Blessing / 第四章 终末祝福` for benediction-style lines.
  - `Appendix I / 附录I` for daily liturgical formulas.
- Choose the single best fit and keep numbering style unchanged.

4. Integrate naturally:
- Match rhythm and diction of adjacent lines.
- Avoid abrupt jumps in tense, register, or theology.
- Insert in mirrored locations in both language files.

5. Commit with explanation:
- Stage only intended files.
- Use a commit title that names oracle insertion.
- Add a detailed commit body describing thematic fit, chapter choice, and interpretive extension.

## Style Rules

- Keep the oracle in one sentence per language.
- Use religious language grounded in mercy, truth, repair, dignity, and service.
- Prefer concrete imagery (bread, light, neighbor, shelter) over abstraction.
- Never contradict existing core claims in the canon.
