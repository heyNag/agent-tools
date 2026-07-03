---
description: Extract setup steps, commands, tools, and implementation checklist from a tutorial video.
argument-hint: <video-url-or-path> [focus]
allowed-tools: [Bash, Read, AskUserQuestion]
---

<!-- charms-managed: watch-video command -->

Use `watch-video` on the tutorial source: $ARGUMENTS

Ask the user which detail level to run first (lightest to heaviest:
`transcript`, `efficient`, `balanced`, `full`) unless the request or
`WATCH_VIDEO_DETAIL` already answers it; recommend `efficient` for command
extraction - spoken content plus keyframes usually carries a tutorial, and
you can re-run a section at `balanced` if a step needs closer frames.

Prefer:

```sh
python3 scripts/watch.py "<source>" --mode tutorial
```

Pin "as you can see" moments with `--timestamps` after reading the
transcript.

For tutorials longer than 10 minutes, ask for a focused section first unless the
user clearly wants a broad skim. Review transcript/captions before extracting
many frames.

Focus on practical extraction:

- tools, services, libraries, and versions mentioned
- setup commands and configuration files
- implementation sequence
- decisions, tradeoffs, and assumptions
- errors or warnings shown on screen
- a short checklist the user can follow

Use timestamps for evidence. Summarize transcript content; paste exact commands
only when visible or spoken clearly enough to be useful.
