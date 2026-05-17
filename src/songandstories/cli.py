from pathlib import Path
import click
from rich.console import Console
from anthropic import Anthropic

from .download import download_audio
from .separate import separate_vocals
from .transcribe import transcribe_lyrics, lines_to_text
from .story import generate_story_questions, collect_story
from .rewrite import rewrite_lyrics
from .synthesize import write_aligned_lyrics, synthesize_vocals_stub
from .mix import mix


@click.command()
@click.argument("youtube_url")
@click.option("--work-dir", default="./work", type=click.Path(), help="Where to put intermediate + final files.")
@click.option("--whisper-model", default="medium", help="Whisper model size (tiny, base, small, medium, large).")
@click.option("--skip-synthesis", is_flag=True, help="Skip vocal synthesis and produce a synced-lyrics file instead.")
def main(youtube_url: str, work_dir: str, whisper_model: str, skip_synthesis: bool):
    """Rewrite a YouTube song's lyrics around your story."""
    console = Console()
    work = Path(work_dir)
    client = Anthropic()

    console.rule("[bold]1. Download")
    audio = download_audio(youtube_url, work / "audio")
    console.print(f"  → {audio}")

    console.rule("[bold]2. Separate vocals")
    vocals, instrumental = separate_vocals(audio, work / "stems")
    console.print(f"  vocals:       {vocals}")
    console.print(f"  instrumental: {instrumental}")

    console.rule("[bold]3. Transcribe lyrics")
    lines = transcribe_lyrics(vocals, model_size=whisper_model)
    lyrics_text = lines_to_text(lines)
    (work / "original_lyrics.txt").write_text(lyrics_text)
    console.print(lyrics_text)

    console.rule("[bold]4. Story")
    questions = generate_story_questions(lyrics_text, client)
    story = collect_story(questions, console)

    console.rule("[bold]5. Rewrite lyrics")
    new_lines = rewrite_lyrics(lines, story, client)
    (work / "new_lyrics.txt").write_text("\n".join(new_lines))
    for ln in new_lines:
        console.print(f"  {ln}")

    console.rule("[bold]6. Synthesize + mix")
    aligned = write_aligned_lyrics(lines, new_lines, work / "aligned_lyrics.txt")
    console.print(f"  aligned lyrics: {aligned}")

    if skip_synthesis:
        console.print("[yellow]Synthesis skipped. Plug in RVC/Suno/etc. in synthesize.py.[/yellow]")
        return

    new_vocals = synthesize_vocals_stub(new_lines, work / "new_vocals.wav")
    if new_vocals.stat().st_size == 0:
        console.print("[yellow]Vocal synthesis is stubbed — no audio produced. See synthesize.py.[/yellow]")
        return

    final = mix(instrumental, new_vocals, work / "final.wav")
    console.print(f"[green]Done:[/green] {final}")


if __name__ == "__main__":
    main()
