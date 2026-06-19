---
name: watch-video
description: Analyze YouTube URLs, local videos, screen recordings, tutorials, demos, and UI bug videos using yt-dlp, ffmpeg, native captions, frame extraction, and Groq Whisper fallback.
argument-hint: "<video-url-or-path> [--start T] [--end T] [question]"
allowed-tools: Bash, Read
homepage: https://github.com/heyNag/agent-tools
repository: https://github.com/heyNag/agent-tools
author: Nagarjuna Boddu
license: MIT
user-invocable: true
---

# watch-video

Use this skill when a user asks you to analyze a video URL, local video, screen
recording, tutorial, demo, UI bug recording, product walkthrough, or any task
where visible UI/actions and spoken content matter.

## Operating Rules

- Prefer native captions/transcripts when available.
- Use `yt-dlp` for URL metadata, captions, and downloading source media.
- Use `ffmpeg`/`ffprobe` for focused audio clips and frame extraction.
- Use Groq Whisper only as a fallback when captions are missing or unavailable.
- Default Groq model: `whisper-large-v3-turbo`.
- Support focused ranges with `--start` and `--end`; use `--duration` when the
  user gives a start plus length.
- Do not paste the full transcript unless the user explicitly asks for it.
- Do not print or expose `GROQ_API_KEY`.
- For long videos, prefer a focused range over a sparse full-video scan.

## Invocation

From this skill directory:

```sh
python3 scripts/watch.py "<source>" --frames
```

Useful options:

```sh
python3 scripts/watch.py "<source>" --start 01:15 --end 02:00 --frames
python3 scripts/watch.py "<source>" --duration 30 --frame-interval 5
python3 scripts/watch.py "<source>" --transcriber none --frames
```

The script writes a run directory under `.watch-video/runs/<run-id>/` and prints
the final `report.md` path.

## Evidence To Use

Read `report.md` first. If frames were extracted, inspect the frame images from
`frames/` before answering visual questions. Use `transcript.md` for spoken
content, but summarize and cite timestamp ranges rather than dumping the full
transcript.

## Response Shape

Unless the user asks for a narrower format, return:

1. Summary
2. Timeline with timestamps
3. Visible UI/actions
4. Commands/tools mentioned
5. Implementation steps or reproduction steps
6. Uncertainty and what would improve confidence

For UI bug videos, include the observed symptom, timestamped evidence, likely
cause, and next debugging checks. For tutorials, extract the commands, tools,
setup steps, decisions, and a compact implementation checklist.

## Failure Handling

- Missing `yt-dlp`: tell the user to run `brew install yt-dlp`.
- Missing `ffmpeg` or `ffprobe`: tell the user to run `brew install ffmpeg`.
- Missing `GROQ_API_KEY`: continue with captions/frames if available and say
  Groq fallback needs `export GROQ_API_KEY=...`.
- Groq API failure: do not retry indefinitely; report the error category and use
  available captions/frames.
- Login-required, private, or region-locked URL: say `yt-dlp` cannot fetch it
  without access and ask for a local file or accessible URL.
