---
description: Analyze a video URL or local video with watch-video.
argument-hint: <video-url-or-path> [question]
allowed-tools: [Bash, Read]
---

Use the `watch-video` skill with the user's arguments: $ARGUMENTS

Run `packages/watch-video/scripts/watch.py` on the source. Prefer captions,
extract a focused audio clip, use Groq Whisper only when captions are missing,
extract frames when visual evidence matters, then answer from `report.md`,
`transcript.md`, and the frame images.

Return a concise summary, timestamped timeline, visible UI/actions,
commands/tools mentioned, implementation or reproduction steps, and uncertainty.
Do not paste the full transcript unless requested.
