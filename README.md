# lecture-to-summary-skills

A Claude Code skill that summarizes university lecture materials — slides (PDF) and transcripts (.txt) — into concise, exam-focused study notes saved as `.md` files.

## Features

- Combines **slides + transcript** into one merged summary
- Flags transcript-only content with ⚠️ (high exam risk — not on slides)
- Keeps your **main Claude Code context clean** by using a subagent for all heavy reading
- Saves summaries as `.md` files next to your lecture materials
- No API key needed — uses your Claude Code subscription

## Installation

```bash
git clone https://github.com/GraceLiao77/lecture-to-summary-skills.git ~/.claude/skills/lecture-to-summary-skills
```

Restart Claude Code — the skill is ready.

## Usage

Just paste your file paths and ask Claude to summarize:

```
summarize '/path/to/slides.pdf' '/path/to/transcript.txt'
```

You can provide any combination of files:
- Slides only (PDF)
- Transcript only (.txt)
- Both slides + transcript (recommended — gives the most complete notes)
- Multiple files at once (e.g. pre-lecture + lecture)

## Output format

The saved `.md` file contains:

| Section | Contents |
|---|---|
| **Key Concepts** | All terms and definitions from slides + transcript |
| **Core Content** | One heading per topic, merging slide points and spoken explanations. ⚠️ flags transcript-only additions |
| **Exam Targets** | Facts, distinctions, and examples the teacher emphasised or repeated |
| **Summary** | 2–3 sentence overview of the lecture |
| **Study Questions** | 5–8 exam-style questions across all materials |

## Example

```
summarize '/Desktop/UOA/Week3-slides.pdf' '/Desktop/UOA/Week3-transcript.txt'
```

Claude will:
1. Spawn a subagent to read and summarize both files
2. Save the result as `summary_Week3.md` in the same folder as your files
3. Tell you the file path — open it in your IDE to review

## Requirements

- [Claude Code](https://claude.ai/code) with an active subscription
- Files must be accessible on your local machine
