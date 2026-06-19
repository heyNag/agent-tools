from __future__ import annotations

import importlib
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def test_modules_importable() -> None:
    assert importlib.import_module("watch")
    assert importlib.import_module("extract_frames")
    assert importlib.import_module("groq_transcribe")


def test_parse_time_and_format_time() -> None:
    extract_frames = importlib.import_module("extract_frames")

    assert extract_frames.parse_time("75") == 75.0
    assert extract_frames.parse_time("01:15") == 75.0
    assert extract_frames.parse_time("1:02:03") == 3723.0
    assert extract_frames.format_time(75) == "01:15"
    assert extract_frames.format_time(3723) == "1:02:03"


def test_resolve_range_duration() -> None:
    extract_frames = importlib.import_module("extract_frames")

    assert extract_frames.resolve_range(10, None, 5) == (10, 15, 5)
    assert extract_frames.resolve_range(None, 30, None) == (0.0, 30, 30)
    assert extract_frames.resolve_range(10, 30, None) == (10, 30, 20)


def test_safe_run_id_is_stable_shape() -> None:
    watch = importlib.import_module("watch")

    run_id = watch.safe_run_id("https://www.youtube.com/watch?v=abc123")
    assert "youtube.com" in run_id
    assert run_id.endswith(watch.safe_run_id("https://www.youtube.com/watch?v=abc123")[-8:])
    assert "?" not in run_id


def test_segments_from_response_offsets() -> None:
    groq = importlib.import_module("groq_transcribe")

    data = {"segments": [{"start": 1, "end": 2.5, "text": " hello "}]}
    assert groq.segments_from_response(data, offset_seconds=10) == [
        {"start": 11.0, "end": 12.5, "text": "hello"}
    ]


def test_transcript_markdown() -> None:
    watch = importlib.import_module("watch")

    text = watch.transcript_markdown([{"start": 5, "end": 6, "text": "hello"}])
    assert text == "[00:05] hello"
