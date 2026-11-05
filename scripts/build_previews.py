"""Copy the four native renders and encode full-length, real-time GIF previews."""

import shutil
import subprocess

from render_all import ROOT, SCENES


def main() -> None:
    (ROOT / "videos").mkdir(exist_ok=True)
    (ROOT / "previews").mkdir(exist_ok=True)
    for module, scene in SCENES:
        source = ROOT / "media" / "videos" / module / "1080p60" / f"{scene}.mp4"
        if not source.is_file():
            raise FileNotFoundError(f"Render {scene} at final quality first.")
        video = ROOT / "videos" / f"{module}.mp4"
        shutil.copy2(source, video)
        # A per-video palette avoids unstable colors and excessive GIF size.
        filters = (
            "fps=15,scale=640:360:flags=lanczos,split[a][b];"
            "[a]palettegen=max_colors=128:stats_mode=diff[p];"
            "[b][p]paletteuse=dither=bayer:bayer_scale=3"
        )
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                str(video),
                "-filter_complex_threads",
                "1",
                "-filter_complex",
                filters,
                "-an",
                "-loop",
                "0",
                str(ROOT / "previews" / f"{module}.gif"),
            ],
            check=True,
        )
        print(f"Prepared videos/{module}.mp4 and previews/{module}.gif")


if __name__ == "__main__":
    main()
