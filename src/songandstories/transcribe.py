from pathlib import Path
from dataclasses import dataclass
import whisper


@dataclass
class LyricLine:
    start: float
    end: float
    text: str


def transcribe_lyrics(vocals_path: Path, model_size: str = "medium") -> list[LyricLine]:
    model = whisper.load_model(model_size)
    result = model.transcribe(str(vocals_path), word_timestamps=False)
    return [
        LyricLine(start=seg["start"], end=seg["end"], text=seg["text"].strip())
        for seg in result["segments"]
    ]


def lines_to_text(lines: list[LyricLine]) -> str:
    return "\n".join(line.text for line in lines)
