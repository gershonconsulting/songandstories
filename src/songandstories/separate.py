import subprocess
from pathlib import Path


def separate_vocals(audio_path: Path, out_dir: Path) -> tuple[Path, Path]:
    """Split audio into vocals + instrumental using Demucs. Returns (vocals, instrumental)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "python", "-m", "demucs.separate",
            "--two-stems", "vocals",
            "-o", str(out_dir),
            "-n", "htdemucs",
            str(audio_path),
        ],
        check=True,
    )
    stem_dir = out_dir / "htdemucs" / audio_path.stem
    return stem_dir / "vocals.wav", stem_dir / "no_vocals.wav"
