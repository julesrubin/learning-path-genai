"""Load prompt templates from `instructions/<name>.txt`."""

from pathlib import Path

_INSTRUCTIONS_DIR = Path(__file__).parent / "instructions"


def load_prompt(name: str, **kwargs: object) -> str:
    """Read `instructions/<name>.txt` and optionally format with kwargs.

    When kwargs are provided, the template is rendered via `str.format`. Use
    doubled braces (`{{` / `}}`) inside the file to emit literal braces.
    """
    template = (_INSTRUCTIONS_DIR / f"{name}.txt").read_text().rstrip("\n")
    return template.format(**kwargs) if kwargs else template
