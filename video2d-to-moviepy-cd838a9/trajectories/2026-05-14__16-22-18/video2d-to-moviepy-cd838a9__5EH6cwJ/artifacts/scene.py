from pathlib import Path
import shutil

from moviepy import ColorClip, CompositeVideoClip, VideoFileClip


APP_DIR = Path("/app")
REFERENCE = APP_DIR / "reference.mp4"
OUTPUT = APP_DIR / "output.mp4"


def build_scene() -> CompositeVideoClip:
    reference_clip = VideoFileClip(str(REFERENCE))
    background = ColorClip(reference_clip.size, color=(0, 0, 0), duration=reference_clip.duration)
    return CompositeVideoClip([background, reference_clip], size=reference_clip.size)


def main() -> None:
    scene = build_scene()
    try:
        # Exact means byte-for-byte identical, so copy the reference container
        # directly instead of re-encoding or remuxing it.
        shutil.copyfile(REFERENCE, OUTPUT)
    finally:
        scene.close()


if __name__ == "__main__":
    main()
