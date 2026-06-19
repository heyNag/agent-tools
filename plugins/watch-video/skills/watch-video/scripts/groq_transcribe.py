#!/usr/bin/env python3
"""Groq Whisper transcription helper using only the Python standard library."""

from __future__ import annotations

import argparse
import io
import json
import mimetypes
import os
import shutil
import subprocess
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GROQ_ENDPOINT = "https://api.groq.com/openai/v1/audio/transcriptions"
DEFAULT_GROQ_MODEL = "whisper-large-v3-turbo"


def _require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is not installed. fix: brew install ffmpeg")


def _read_key(api_key: str | None = None) -> str:
    key = api_key or os.environ.get("GROQ_API_KEY", "")
    key = key.strip()
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. fix: export GROQ_API_KEY=... "
            "or add it to your local shell environment"
        )
    return key


def extract_audio_clip(
    source: str | Path,
    out_path: str | Path,
    *,
    start: float | None = None,
    end: float | None = None,
    duration: float | None = None,
) -> Path:
    """Extract a mono 16 kHz MP3 audio clip suitable for Whisper."""
    _require_ffmpeg()
    if end is not None and duration is not None:
        raise ValueError("use either end or duration, not both")
    if start is not None and start < 0:
        raise ValueError("start must be non-negative")
    if end is not None and start is not None and end <= start:
        raise ValueError("end must be greater than start")
    if duration is not None and duration <= 0:
        raise ValueError("duration must be greater than zero")

    output = Path(out_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if start is not None:
        cmd.extend(["-ss", f"{start:.3f}"])
    cmd.extend(["-i", str(source)])
    if duration is not None:
        cmd.extend(["-t", f"{duration:.3f}"])
    elif start is not None and end is not None:
        cmd.extend(["-t", f"{end - start:.3f}"])
    elif start is None and end is not None:
        cmd.extend(["-t", f"{end:.3f}"])
    cmd.extend(
        [
            "-vn",
            "-acodec",
            "libmp3lame",
            "-ar",
            "16000",
            "-ac",
            "1",
            "-b:a",
            "64k",
            str(output),
        ]
    )

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or "unknown ffmpeg error"
        raise RuntimeError(f"ffmpeg audio extraction failed: {detail}")
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("ffmpeg produced no audio; the source may have no audio track")
    return output


def _multipart_body(fields: dict[str, str], audio_path: Path) -> tuple[bytes, str]:
    boundary = f"----WatchVideo{uuid.uuid4().hex}"
    eol = b"\r\n"
    body = io.BytesIO()

    for key, value in fields.items():
        body.write(f"--{boundary}".encode())
        body.write(eol)
        body.write(f'Content-Disposition: form-data; name="{key}"'.encode())
        body.write(eol)
        body.write(eol)
        body.write(str(value).encode())
        body.write(eol)

    mimetype = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
    body.write(f"--{boundary}".encode())
    body.write(eol)
    body.write(
        f'Content-Disposition: form-data; name="file"; filename="{audio_path.name}"'.encode()
    )
    body.write(eol)
    body.write(f"Content-Type: {mimetype}".encode())
    body.write(eol)
    body.write(eol)
    body.write(audio_path.read_bytes())
    body.write(eol)
    body.write(f"--{boundary}--".encode())
    body.write(eol)

    return body.getvalue(), boundary


def _error_detail(exc: HTTPError) -> str:
    try:
        payload = exc.read().decode("utf-8", errors="replace")
    except Exception:
        payload = ""
    return f" - {payload[:500]}" if payload else ""


def transcribe_audio(
    audio_path: str | Path,
    *,
    out_json: str | Path | None = None,
    model: str | None = None,
    api_key: str | None = None,
    endpoint: str = GROQ_ENDPOINT,
) -> dict:
    """POST an audio file to Groq and optionally save the verbose JSON response."""
    key = _read_key(api_key)
    audio = Path(audio_path).expanduser().resolve()
    if not audio.exists():
        raise RuntimeError(f"audio file not found: {audio}")

    fields = {
        "model": model or os.environ.get("GROQ_MODEL") or DEFAULT_GROQ_MODEL,
        "response_format": "verbose_json",
        "temperature": "0",
    }
    body, boundary = _multipart_body(fields, audio)
    request = Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "agent-tools-watch-video/0.1",
        },
    )

    try:
        with urlopen(request, timeout=300) as response:
            payload = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        raise RuntimeError(f"Groq transcription failed: HTTP {exc.code}{_error_detail(exc)}") from exc
    except URLError as exc:
        raise RuntimeError(f"Groq transcription failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError("Groq transcription timed out") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Groq returned non-JSON response: {payload[:200]}") from exc

    if out_json is not None:
        out_path = Path(out_json).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def segments_from_response(data: dict, *, offset_seconds: float = 0.0) -> list[dict[str, object]]:
    """Convert Groq verbose_json into normalized transcript segments."""
    segments: list[dict[str, object]] = []
    for segment in data.get("segments") or []:
        text = str(segment.get("text") or "").strip()
        if not text:
            continue
        start = float(segment.get("start") or 0.0) + offset_seconds
        end = float(segment.get("end") or 0.0) + offset_seconds
        segments.append(
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "text": text,
            }
        )

    if not segments:
        text = str(data.get("text") or "").strip()
        if text:
            segments.append(
                {
                    "start": round(offset_seconds, 3),
                    "end": round(offset_seconds, 3),
                    "text": text,
                }
            )
    return segments


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audio with Groq Whisper.")
    parser.add_argument("audio_file", help="Audio file to transcribe")
    parser.add_argument("--out", help="Path for the raw JSON response")
    parser.add_argument(
        "--model",
        default=os.environ.get("GROQ_MODEL") or DEFAULT_GROQ_MODEL,
        help=f"Groq Whisper model (default: {DEFAULT_GROQ_MODEL})",
    )
    parser.add_argument("--quiet", action="store_true", help="Do not print JSON to stdout")
    args = parser.parse_args()

    try:
        data = transcribe_audio(args.audio_file, out_json=args.out, model=args.model)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    if not args.quiet:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
