from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class OutgoingMessage:

    text: str

    media_path: Optional[Path] = None

    media_type: Optional[str] = None