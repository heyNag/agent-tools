---
description: Analyze a UI bug or screen recording with timestamped visual evidence.
argument-hint: <video-url-or-path> [expected behavior]
allowed-tools: [Bash, Read, AskUserQuestion]
---

<!-- charms-managed: watch-video command -->

Use `watch-video` on the UI bug recording: $ARGUMENTS

Ask the user which detail level to run first (lightest to heaviest:
`transcript`, `efficient`, `balanced`, `full`) unless the request or
`WATCH_VIDEO_DETAIL` already answers it; recommend `balanced` - UI bugs need
frames that land on the moments the screen changes.

Prefer:

```sh
python3 scripts/watch.py "<source>" --mode ui-bug --frame-format png --resolution 1024
```

Screen recordings that barely change fall back to uniform sampling and
collapse near-duplicate frames automatically. After reading the transcript,
pin exact failure moments with `--timestamps` if scene detection missed them.

For recordings longer than 10 minutes, ask for or infer the relevant repro
window first. For videos longer than 30 seconds, inspect transcript/captions
before extracting a dense frame set.

Inspect frames closely and align them with the transcript if audio is present.
Return:

- observed symptom
- expected behavior if the user provided it
- timestamped evidence
- visible UI state, cursor/action sequence, and transitions
- likely cause ranked by confidence
- concrete next debugging checks
- uncertainty and missing evidence

Avoid over-claiming. If the video does not show enough detail, name the missing
logs, code path, browser console, network request, or repro step needed next.
