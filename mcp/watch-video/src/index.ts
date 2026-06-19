import readline from "node:readline";

type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | { [key: string]: JsonValue };

type JsonRpcRequest = {
  jsonrpc?: string;
  id?: string | number | null;
  method?: string;
  params?: Record<string, unknown>;
};

const serverInfo = {
  name: "watch-video",
  version: "0.1.0"
};

function writeMessage(message: JsonValue): void {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function result(id: JsonRpcRequest["id"], value: JsonValue): void {
  if (id === undefined) {
    return;
  }
  writeMessage({ jsonrpc: "2.0", id, result: value });
}

function error(id: JsonRpcRequest["id"], code: number, message: string): void {
  if (id === undefined) {
    return;
  }
  writeMessage({ jsonrpc: "2.0", id, error: { code, message } });
}

function statusPayload(): JsonValue {
  return { ok: true, name: "watch-video" };
}

function handleToolsCall(request: JsonRpcRequest): void {
  const params = request.params ?? {};
  const name = params.name;
  if (name !== "watch_video_status") {
    error(request.id, -32602, `unknown tool: ${String(name)}`);
    return;
  }

  result(request.id, {
    content: [
      {
        type: "text",
        text: JSON.stringify(statusPayload())
      }
    ]
  });
}

function handleRequest(request: JsonRpcRequest): void {
  switch (request.method) {
    case "initialize":
      result(request.id, {
        protocolVersion: "2024-11-05",
        capabilities: {
          tools: {}
        },
        serverInfo
      });
      break;

    case "notifications/initialized":
      break;

    case "ping":
      result(request.id, {});
      break;

    case "tools/list":
      result(request.id, {
        tools: [
          {
            name: "watch_video_status",
            description: "Return basic watch-video MCP placeholder status.",
            inputSchema: {
              type: "object",
              additionalProperties: false,
              properties: {}
            }
          }
        ]
      });
      break;

    case "tools/call":
      handleToolsCall(request);
      break;

    default:
      error(request.id, -32601, `method not found: ${String(request.method)}`);
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  crlfDelay: Infinity
});

rl.on("line", (line: string) => {
  if (!line.trim()) {
    return;
  }

  let request: JsonRpcRequest;
  try {
    request = JSON.parse(line) as JsonRpcRequest;
  } catch {
    writeMessage({
      jsonrpc: "2.0",
      id: null,
      error: { code: -32700, message: "parse error" }
    });
    return;
  }

  if (!request.method) {
    error(request.id, -32600, "invalid request");
    return;
  }

  handleRequest(request);
});
