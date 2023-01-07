from dataclasses import dataclass, field


@dataclass
class Style:

    # Subject: The main character of the card.
    subject: str = None
    subject_type: str = "monster"
    subject_adjectives: list[str] = field(default_factory=list)

    # Detail: Something describing the subject.
    detail: str | None = None
    detail_adjective: str | None = None

    # Environments, background and ambience.
    environment: str | None = None
    background: str | None = None
    ambience: str | None = None

    # The name of the style.
    style_prefix: str = ""
    style_suffix: str = ""
