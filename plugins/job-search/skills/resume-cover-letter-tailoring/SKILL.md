---
name: resume-cover-letter-tailoring
description: Tailor Joseph's resume and draft a cover letter for a specific job posting (URL or pasted description). Uses only real experience from the base resume, outputs two .docx files.
---

Run this when Joseph provides a specific job posting (a URL and/or pasted job description). Produce a tailored resume and cover letter for it.

## Config

- Candidate: Joseph Alfonso, product/UX designer. Portfolio https://josephalfonso.com/, LinkedIn https://www.linkedin.com/in/jalfonsodesign/
- Base resume folder: `~/Documents/JobSearch` (any .docx, .pdf, .txt or .md with "Resume" in the name)

## Steps

1. Base resume: read the resume from the folder above to get his real experience, skills and background. If none is found, ask Joseph for his resume content before going further. Never fabricate experience.

2. Job posting: if given a URL, fetch it (web fetch, or browser tools for JS-heavy pages). If pasted text was given, use it directly.

3. Tailor the resume: reorder and re-emphasize bullets and skills from his real background to match the posting's language and priorities. Don't invent experience, tools or accomplishments. Keep it one page unless the base resume is longer.

4. Draft a cover letter: 3-4 short paragraphs, specific to the company and role, grounded in his actual background, no generic filler. No em dashes (use commas), direct and plainspoken. If the `write-like-joseph` skill is available, run its voice pass.

5. Load the `docx` skill for formatting guidance. Save both as .docx in the outputs folder: `{Company}_{Role}_Resume.docx` and `{Company}_{Role}_CoverLetter.docx`. Never overwrite the base resume.

6. Present both files and give a one-line summary of what was emphasized and why.
