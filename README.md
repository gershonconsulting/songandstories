# songandstories

Rewrite a YouTube song's lyrics around your own story, then (eventually) re-sing it in the original singer's voice.

## Pipeline

1. **Download** the YouTube audio (`yt-dlp`)
2. **Separate** vocals from instrumental (`demucs`)
3. **Transcribe** the lyrics with timings (`whisper`)
4. **Ask** the user story questions tailored to the song (Claude)
5. **Rewrite** the lyrics to fit the story, preserving meter (Claude)
6. **Synthesize** new vocals — *stubbed*; plug in RVC / So-VITS-SVC / Suno here
7. **Mix** new vocals over the original instrumental (`pydub` / `ffmpeg`)

## Install

```bash
pip install -e .
# Requires ffmpeg installed on the system.
export ANTHROPIC_API_KEY=...
```

## Run

```bash
songandstories "https://www.youtube.com/watch?v=..." --work-dir ./work
# To stop before the (stubbed) vocal synthesis and just produce aligned lyrics:
songandstories "<url>" --skip-synthesis
```

## Status

Steps 1-5 and 7 are real. Step 6 is a stub — see `src/songandstories/synthesize.py`. Singing voice cloning of a real artist is also a legal/ethics gray area; this is for personal experimentation.
