---
description: Analyze a video URL or local video with watch-video.
argument-hint: <video-url-or-path> [question]
allowed-tools: [Bash, Read, AskUserQuestion]
---

<!-- charms-managed: watch-video command -->

Use the `watch-video` skill with the user's arguments: $ARGUMENTS

Run the `watch.py` script from the installed `watch-video` skill, or
`packages/watch-video/skills/watch-video/scripts/watch.py` when working from
this repository.

First ask the user which detail level to run for this video (AskUserQuestion
on Claude Code), offering lightest to heaviest: `transcript` (fastest, no
frames), `efficient` (keyframe skim, cap 50), `balanced` (Recommended -
scene-aware, cap 80), `full` (every scene change, cap 300, high token cost).
Skip the question when the request already implies a level, `--detail` was
given, `WATCH_VIDEO_DETAIL` is set, it is a re-run of the same video, or
nobody can answer - then use `balanced` and say so. Captions are preferred
automatically; Groq Whisper runs only when captions are missing or weak. If
transcription is needed and no key exists, ask once (Groq recommended) and
store it with `python3 scripts/doctor.py --set-key groq` from stdin - never
echo the key. Near-duplicate frames are dropped automatically.

For videos longer than 10 minutes, ask for or infer a focused range first
(`--start/--end`). After reading the transcript, pin any presenter-flagged
moments with `--timestamps` against the downloaded media file. Use
`--frame-format png --resolution 1024` when screen/UI text needs to be
readable.

Read every extracted frame with parallel Read calls, then answer with a
concise summary, timestamped timeline, visible UI/actions, commands/tools
mentioned, implementation or reproduction steps, and uncertainty. Do not paste
the full transcript unless requested, and do not re-run the script for
follow-up questions.
