"""Voice synthesis stub.

Singing voice synthesis that matches the original singer is the hardest part of
the pipeline. Real options: RVC, So-VITS-SVC, Suno API, Musicfy. This module
ships a placeholder that writes the new lyrics aligned to the original timings,
and (optionally) generates plain TTS audio so the rest of the pipeline is
end-to-end testable. Swap in real singing synthesis here.
"""
from pathlib import Path
from .transcribe import LyricLine


def write_aligned_lyrics(lines: list[LyricLine], new_text: list[str], out_path: Path) -> Path:
    """Write a synced-lyrics text file: [start - end] new_line."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        for line, new in zip(lines, new_text):
            f.write(f"[{line.start:6.2f} - {line.end:6.2f}]  {new}\n")
    return out_path


def synthesize_vocals_stub(new_text: list[str], out_path: Path) -> Path:
    """Placeholder: returns the path without producing audio.
    Replace with a call to RVC / Suno / etc.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(b"")
    return out_path
