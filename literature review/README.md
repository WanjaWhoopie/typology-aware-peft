# Literature

Everything to do with the papers we read.

```
literature review/
├── README.md           # this file
├── TEMPLATE.md         # copy this for each new paper
├── reading-log.md      # index of every paper, read or queued
├── gaps-and-ideas.md   # gaps, themes and ideas collected across papers
├── notes/              # one markdown file per paper
└── papers/             # PDFs (kept locally, not pushed to GitHub)
```

## Adding a paper

1. Optionally keep a local PDF copy in `papers/`. The note must always link to the paper online.
2. Copy `TEMPLATE.md` into `notes/` and name it `YYYY-firstauthor-shortname.md`, for example `2024-ndomba-swahili-tokenizer.md`.
3. Add a row to `reading-log.md` with status 📥 To read.
4. Fill in the note as you read, then update the status in the log.
5. Copy any strong gaps or ideas into `gaps-and-ideas.md`.

## Why the PDFs are not on GitHub

Most papers are under publisher copyright, so `.gitignore` excludes `literature review/papers/*.pdf`. Every note links to the paper online (DOI, arXiv, or publisher/repository page) so anyone can open it.
