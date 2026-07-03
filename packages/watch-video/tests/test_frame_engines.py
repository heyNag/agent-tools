"""Frame-engine integration tests against ffmpeg-synthesized clips.

These build tiny lavfi color clips (hard cuts force keyframes and scene
changes) so the scene, keyframe, uniform-fallback, dedup, and cue paths run
against real ffmpeg output with no network and no fixtures. Skipped when
ffmpeg/ffprobe are unavailable (for example on bare CI runners).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "watch-video" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import extract_frames  # noqa: E402


HAVE_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

COLORS = ["red", "green", "blue", "white", "black", "yellow", "cyan", "magenta", "gray", "orange"]


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg setup failed: {result.stderr.strip()[:400]}")


def build_cut_clip(path: Path, colors: int = 10, segment: float = 0.4) -> None:
    """Concatenate solid-color segments; every color change is a hard cut."""
    inputs: list[str] = []
    for index in range(colors):
        inputs += [
            "-f", "lavfi", "-t", str(segment),
            "-i", f"color=c={COLORS[index % len(COLORS)]}:s=160x120:r=10",
        ]
    streams = "".join(f"[{index}:v]" for index in range(colors))
    graph = f"{streams}concat=n={colors}:v=1:a=0[out]"
    _run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        *inputs,
        "-filter_complex", graph, "-map", "[out]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-force_key_frames", f"expr:gte(t,n_forced*{segment})",
        str(path),
    ])


def build_static_clip(path: Path, duration: float = 3.0) -> None:
    """One solid color: no scene changes, one keyframe -> both fallbacks."""
    _run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-t", str(duration), "-i", "color=c=blue:s=160x120:r=10",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "600",
        str(path),
    ])


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe not installed")
class FrameEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        base = Path(cls._tmp.name)
        cls.cut_clip = base / "cuts.mp4"
        cls.static_clip = base / "static.mp4"
        build_cut_clip(cls.cut_clip)
        build_static_clip(cls.static_clip)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_scene_engine_finds_cuts_with_exact_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_scene_frames(
                self.cut_clip, tmp, max_frames=100, dedup=False
            )

        self.assertEqual(meta["engine"], "scene")
        self.assertFalse(meta["fallback"])
        self.assertGreaterEqual(len(frames), extract_frames.SCENE_MIN_FRAMES)
        self.assertEqual(frames[0]["reason"], "first-frame")
        self.assertTrue(all(frame["reason"] == "scene-change" for frame in frames[1:]))
        timestamps = [frame["timestamp_seconds"] for frame in frames]
        self.assertEqual(timestamps, sorted(timestamps))
        self.assertGreater(timestamps[-1], timestamps[0])

    def test_scene_engine_falls_back_to_uniform_on_static_video(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_scene_frames(
                self.static_clip, tmp, max_frames=100, dedup=False
            )

        self.assertEqual(meta["engine"], "uniform")
        self.assertTrue(meta["fallback"])
        self.assertGreaterEqual(len(frames), 1)
        self.assertTrue(all(frame["reason"] == "uniform" for frame in frames))

    def test_dedup_collapses_static_uniform_frames(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_scene_frames(
                self.static_clip, tmp, max_frames=100, dedup=True
            )

        self.assertTrue(meta["fallback"])
        self.assertGreaterEqual(int(meta["deduped_count"]), 1)
        self.assertEqual(len(frames), 1)

    def test_keyframe_engine_reads_forced_keyframes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_keyframes(
                self.cut_clip, tmp, max_frames=50, dedup=False
            )

        self.assertEqual(meta["engine"], "keyframe")
        self.assertFalse(meta["fallback"])
        self.assertGreaterEqual(len(frames), extract_frames.KEYFRAME_MIN)
        self.assertTrue(all(frame["reason"] == "keyframe" for frame in frames))

    def test_keyframe_engine_falls_back_when_keyframes_are_sparse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_keyframes(
                self.static_clip, tmp, max_frames=50, dedup=False
            )

        self.assertEqual(meta["engine"], "uniform")
        self.assertTrue(meta["fallback"])
        self.assertGreaterEqual(len(frames), 1)

    def test_even_sample_cap_keeps_first_and_last(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            all_frames, _ = extract_frames.extract_scene_frames(
                self.cut_clip, tmp, max_frames=100, dedup=False
            )
        with tempfile.TemporaryDirectory() as tmp:
            capped, meta = extract_frames.extract_scene_frames(
                self.cut_clip, tmp, max_frames=5, dedup=False
            )

        self.assertEqual(len(capped), 5)
        self.assertEqual(meta["selected_count"], 5)
        self.assertAlmostEqual(
            capped[0]["timestamp_seconds"], all_frames[0]["timestamp_seconds"], places=1
        )
        self.assertAlmostEqual(
            capped[-1]["timestamp_seconds"], all_frames[-1]["timestamp_seconds"], places=1
        )

    def test_extract_at_timestamps_pins_cue_frames(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_at_timestamps(
                self.cut_clip,
                tmp,
                [0.2, 1.4, 99.0],
                window_start=None,
                window_end=3.9,
            )

        self.assertEqual(meta["dropped_out_of_window"], 1)
        self.assertEqual(len(frames), 2)
        self.assertTrue(all(frame["reason"] == "transcript-cue" for frame in frames))
        self.assertTrue(all(Path(str(frame["path"])).name.startswith("cue_") for frame in frames))
        self.assertEqual(
            [frame["timestamp_seconds"] for frame in frames],
            [0.2, 1.4],
        )

    def test_uniform_engine_reports_meta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames, meta = extract_frames.extract_frames(
                self.cut_clip, tmp, max_frames=10, dedup=False
            )

        self.assertEqual(meta["engine"], "uniform")
        self.assertEqual(meta["selected_count"], len(frames))
        self.assertTrue(all(frame["reason"] == "uniform" for frame in frames))


if __name__ == "__main__":
    unittest.main()
