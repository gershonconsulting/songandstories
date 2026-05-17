from pathlib import Path
from pydub import AudioSegment


def mix(instrumental: Path, vocals: Path, out_path: Path) -> Path:
    inst = AudioSegment.from_file(instrumental)
    voc = AudioSegment.from_file(vocals)
    if len(voc) < len(inst):
        voc = voc + AudioSegment.silent(duration=len(inst) - len(voc))
    combined = inst.overlay(voc)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    combined.export(out_path, format="wav")
    return out_path
