from anthropic import Anthropic
from .transcribe import LyricLine

MODEL = "claude-opus-4-7"

REWRITE_PROMPT = """You are a skilled lyricist. Rewrite the following song's lyrics so they tell the user's personal story, while preserving the original meter, rhyme scheme, line count, and emotional arc.

Original lyrics (one line per segment, in order):
<lyrics>
{numbered_lyrics}
</lyrics>

The user's story:
<story>
{story}
</story>

Rules:
- Output exactly the same number of lines as the original.
- Match syllable count per line as closely as possible so it can be sung to the same melody.
- Preserve choruses (repeated lines should still repeat).
- Keep the same rhyme positions.
- Output ONLY the new lyrics, one line per original line, no numbering, no explanation."""


def rewrite_lyrics(lines: list[LyricLine], story: dict[str, str], client: Anthropic) -> list[str]:
    numbered = "\n".join(f"{i+1}. {line.text}" for i, line in enumerate(lines))
    story_text = "\n".join(f"- {q} {a}" for q, a in story.items())
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": REWRITE_PROMPT.format(numbered_lyrics=numbered, story=story_text),
        }],
    )
    text = resp.content[0].text.strip()
    new_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(new_lines) != len(lines):
        new_lines = (new_lines + [""] * len(lines))[:len(lines)]
    return new_lines
