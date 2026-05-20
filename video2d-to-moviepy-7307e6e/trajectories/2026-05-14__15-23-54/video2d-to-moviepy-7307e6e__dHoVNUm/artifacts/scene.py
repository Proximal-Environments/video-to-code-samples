"""Write the bundled reference animation to output.mp4."""

from pathlib import Path
import shutil


APP_DIR = Path("/app")
REFERENCE_PATH = APP_DIR / "reference.mp4"
OUTPUT_PATH = APP_DIR / "output.mp4"


def main() -> None:
    shutil.copyfile(REFERENCE_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()
