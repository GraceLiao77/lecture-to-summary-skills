---
name: lecture-to-summary-skills
description: Summarizes university lecture materials (PDFs, transcripts, pre-lecture notes) into structured study notes saved as .md files. Uses Claude Code subscription — no API credits needed.
---

# Lecture Summarizer

All heavy work (reading raw files, summarizing, saving) runs in a **subagent** so the main context stays clean. The main context only reads the final saved `.md` summary.

## When to use

Activate this skill when the user:
- Says "summarize this lecture / week / reading"
- Provides file paths to PDFs, transcripts (.txt), or pre-lecture notes
- Asks for study notes or revision notes from course materials

## Instructions

### Step 1 — Check if a summary already exists

Use the Glob tool to check if a summary `.md` already exists:

```
<original_file_dir>/summary_Week*.md
```

- If it **exists**: tell the user the summary already exists at that path and offer to answer questions about it. **Do NOT read the file into context unless the user asks a specific question.** Stop here — do not spawn an agent.
- If it **does not exist**: proceed to Step 2.

### Step 2 — Spawn a subagent to do all the work

Use the **Agent tool** (subagent_type: `general-purpose`) to handle reading the raw files, generating the summary, and saving the `.md`. Pass a self-contained prompt like this:

```
Read the following lecture file(s) and produce comprehensive study notes, then save them.

FILES:
- <file_path_1>
- <file_path_2>  (if multiple)

OUTPUT FILE: <same_directory>/summary_<WeekN>.md

GOAL: Produce revision notes that are concise enough to read quickly, but complete enough that nothing examinable is missed. Do NOT reproduce the transcript verbatim. Distil — compress each idea to its sharpest form.

RULES:
- Use slides as the structural backbone.
- Use the transcript to find: extra definitions, examples, caveats, and anything the teacher emphasised or repeated — these are likely exam targets.
- Every point must earn its place. If it won't help the student answer an exam question, cut it.
- No long paragraphs. Use short bullet points. Max 2 sentences per bullet.
- Do not repeat the same point in multiple sections.
- For examples: state what the example shows in 1–2 sentences. Do not retell the full story.
- For references: author + year + one-line takeaway only. No journal volume/page details.

Use this exact format for the output:

# [Week N] — [Topic Title]

## Key Concepts
- **Term** — one-sentence definition. Include all terms from slides AND any additional ones the teacher defined verbally.

## Core Content
For each major topic from the slides (use ### headings):
### [Topic Name]
- Bullet points merging slide content + transcript detail
- Flag transcript-only additions with ⚠️ (these are high exam risk since they're not on the slides)
- Keep each bullet to 1–2 sentences max

## Exam Targets
- Specific facts, definitions, distinctions, or examples the teacher emphasised, repeated, or explicitly called out
- Each item = one concise bullet. Format: **what it is** — why it matters / what to remember about it

## Summary
2–3 sentences: what this lecture is about and the single most important takeaway.

## Study Questions
5–8 questions that cover both slide content and transcript-only content. These should be the kind of questions likely to appear on an exam.

---

Save the completed summary using the Write tool to: <output_file_path>
Report back: "Done. Saved to <output_file_path>"
```

Wait for the agent to finish.

### Step 3 — Confirm and tell the user where to find it

After the subagent completes, **do NOT read the saved `.md` file**. Just tell the user:
- The file was saved successfully
- The full path to the `.md` file
- A 2–3 line plain-English description of what was captured (e.g. how many sections, whether transcript-only content was found)

Do not load the file contents into the main context. The user can open it directly in the IDE.

### Step 4 — Offer follow-up

After presenting the summary, offer to:
- Explain any concept in more depth
- Generate flashcards from the key concepts
- Quiz the user with the study questions

> **Note:** Flashcards and quizzes should also be done inline (small, no raw file reading needed). Only summarization of raw lecture files uses a subagent.

## Searching a specific lecture

When the user asks to find or review a specific lecture topic:
1. Use Glob to find matching `summary_Week*.md` files in the relevant directory.
2. Use Grep to search for the specific keyword/topic inside those files — load only the matching lines, not the whole file.
3. Answer from those excerpts. Only use Read on the full file if the question genuinely requires broader context that Grep cannot provide.
