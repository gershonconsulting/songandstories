import json
from anthropic import Anthropic
from rich.prompt import Prompt
from rich.console import Console

MODEL = "claude-opus-4-7"

QUESTIONS_PROMPT = """You are helping a user personalize a song by rewriting its lyrics around their own story.

Here are the original lyrics:
<lyrics>
{lyrics}
</lyrics>

Generate 4-6 short, specific questions that will gather the details needed to rewrite these lyrics meaningfully. Tailor the questions to the song's themes and structure (verses, chorus, mood).

Respond with ONLY a JSON array of question strings, no other text. Example: ["Who is the song about?", "What happened between you?"]"""


def generate_story_questions(lyrics: str, client: Anthropic) -> list[str]:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": QUESTIONS_PROMPT.format(lyrics=lyrics)}],
    )
    text = resp.content[0].text.strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


def collect_story(questions: list[str], console: Console) -> dict[str, str]:
    console.print("\n[bold cyan]Tell me your story:[/bold cyan]\n")
    answers = {}
    for q in questions:
        answers[q] = Prompt.ask(f"[yellow]{q}[/yellow]")
    return answers
