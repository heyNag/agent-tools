# watch-video MCP Placeholder

This is a minimal deployable MCP server shape for future `watch-video` work.
It intentionally does not wrap the video processing scripts yet and it is not an
MCP gateway.

Current tool:

- `watch_video_status` - returns `{ "ok": true, "name": "watch-video" }`

## Development

```sh
npm run build
npm start
```

This placeholder currently has no npm dependencies, which keeps CI offline and
no-secret. The server speaks JSON-RPC over stdio and implements only the small
subset needed for the status tool. A future version can replace this manual
skeleton with the official MCP SDK once the video-processing API surface is
clear.
