"""Decode every exported video/GIF and write a portable validation record.

This checks encoding and frame geometry. It does not claim to replace human
inspection of mathematical legibility or transitions.
"""

import hashlib
import json
import subprocess
from fractions import Fraction

import numpy as np
from PIL import Image, ImageSequence
from render_all import ROOT, SCENES


def probe(path) -> dict:
    return json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ]
        )
    )


def validate_video(path) -> dict:
    metadata = probe(path)
    assert len(metadata["streams"]) == 1, "Expected one silent video stream."
    stream = metadata["streams"][0]
    assert stream["codec_type"] == "video" and stream["codec_name"] == "h264"
    assert (stream["width"], stream["height"]) == (1920, 1080)
    assert Fraction(stream["avg_frame_rate"]) == 60
    assert stream["pix_fmt"] == "yuv420p"
    timestamps = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_frames",
                "-show_entries",
                "frame=best_effort_timestamp_time",
                "-of",
                "json",
                str(path),
            ]
        )
    )["frames"]
    pts = np.array([float(frame["best_effort_timestamp_time"]) for frame in timestamps])
    assert np.max(np.abs(np.diff(pts) - 1 / 60)) < 0.000002
    frame_bytes = 320 * 180 * 3
    count, leading_blank = 0, []
    with subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-an",
            "-vf",
            "scale=320:180",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
    ) as decoder:
        while True:
            data = decoder.stdout.read(frame_bytes)
            if not data:
                break
            assert len(data) == frame_bytes
            image = (
                np.frombuffer(data, dtype=np.uint8)
                .reshape(180, 320, 3)
                .astype(np.int16)
            )
            background = np.median(image[:2, :8], axis=(0, 1))
            active = np.max(np.abs(image - background), axis=2) > 25
            if active.sum() < 10:
                # The title fades in from the background; allow only a short leading prefix.
                assert count < 15 and len(leading_blank) == count, (
                    f"Unexpected empty frame: {count}"
                )
                leading_blank.append(count)
            border = np.concatenate(
                [
                    active[:2].ravel(),
                    active[-2:].ravel(),
                    active[:, :2].ravel(),
                    active[:, -2:].ravel(),
                ]
            )
            assert not border.any(), f"Foreground reaches outer frame border at {count}"
            count += 1
        assert decoder.wait() == 0
    assert count == len(pts) == int(stream["nb_frames"])
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "resolution": [1920, 1080],
        "fps": 60,
        "frames_decoded": count,
        "duration_seconds": count / 60,
        "codec": "H.264 / yuv420p",
        "audio_streams": 0,
        "unexpected_blank_frames": 0,
        "clipped_border_frames": 0,
        "initial_fade_blank_frames": leading_blank,
        "timestamp_check": "Every frame advances by 1/60 second.",
    }


def main() -> None:
    results = []
    for module, scene in SCENES:
        row = validate_video(ROOT / "videos" / f"{module}.mp4")
        path = ROOT / "previews" / f"{module}.gif"
        durations = []
        with Image.open(path) as gif:
            assert gif.size == (640, 360) and gif.info.get("loop") == 0
            for frame in ImageSequence.Iterator(gif):
                frame.convert("RGB").load()
                durations.append(frame.info.get("duration", 0) / 1000)
        assert len(durations) > 1 and all(t > 0 for t in durations)
        assert abs(sum(durations) - row["duration_seconds"]) < 0.15
        row["gif"] = {
            "file": f"previews/{module}.gif",
            "frames_decoded": len(durations),
            "resolution": [640, 360],
            "duration_seconds": round(sum(durations), 3),
            "bytes": path.stat().st_size,
        }
        row["scene"] = scene
        results.append(row)
    report = {
        "status": "passed",
        "renderer": "Manim Community 0.19.0 / Cairo",
        "videos": results,
        "scope": "Full video/GIF decoding and format checks. Manual review is documented separately.",
    }
    (ROOT / "docs" / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
