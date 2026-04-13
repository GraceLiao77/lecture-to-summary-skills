#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3
"""
Lecture Summarizer — processes PDFs, transcripts, and pre-lecture materials
via the Anthropic API in a separate call so the main conversation context stays clean.

Usage:
  python summarize.py file1.pdf file2.txt file3.pdf
  python summarize.py --week "Week 3" slides.pdf transcript.txt reading.pdf
"""

import sys
import os
import base64
import argparse
import anthropic

SUMMARY_PROMPT = """You are a university study assistant. Summarize the provided lecture material(s) into structured study notes.

For each file/document, produce:

## [Topic / File Name]

**Key Concepts**
- Bullet list of 5–10 core concepts, terms, or definitions introduced

**Main Points**
1. Numbered list of the central arguments or explanations in logical order

**Important Details**
- Formulas, models, frameworks, specific facts, names, or dates worth memorizing

**Summary**
2–3 sentences explaining what this material covers and why it matters.

**Study Questions**
1. 3–5 questions a student should be able to answer after reviewing this material

---

If multiple files are provided, after individual summaries add a:

## Combined Week Summary
- What themes connect across all materials
- The 3 most important takeaways overall
- Any gaps or contradictions between materials

Keep language clear and concise. Define jargon when first used."""


def encode_pdf(path: str) -> dict:
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": data,
        },
        "title": os.path.basename(path),
    }


def read_text(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {
        "type": "text",
        "text": f"=== {os.path.basename(path)} ===\n\n{content}",
    }


def build_content(files: list[str]) -> list[dict]:
    content = []
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            content.append(encode_pdf(path))
        else:
            content.append(read_text(path))
    content.append({"type": "text", "text": SUMMARY_PROMPT})
    return content


def main():
    parser = argparse.ArgumentParser(description="Summarize lecture materials via Claude API")
    parser.add_argument("files", nargs="+", help="PDF, .txt, or .md files to summarize")
    parser.add_argument("--week", help="Optional week label (e.g. 'Week 3')", default=None)
    parser.add_argument("--model", default="claude-opus-4-6", help="Claude model to use")
    args = parser.parse_args()

    # Validate files exist
    for f in args.files:
        if not os.path.exists(f):
            print(f"Error: file not found: {f}", file=sys.stderr)
            sys.exit(1)

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    label = f" — {args.week}" if args.week else ""
    print(f"\nSummarizing {len(args.files)} file(s){label}...\n")

    message = client.messages.create(
        model=args.model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": build_content(args.files),
            }
        ],
    )

    summary = message.content[0].text
    print(summary)

    # Optionally save to file
    out_name = f"summary{'_' + args.week.replace(' ', '_') if args.week else ''}.md"
    out_path = os.path.join(os.path.dirname(args.files[0]), out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Lecture Summary{label}\n\n")
        f.write(summary)
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
