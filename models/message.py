from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ChatInfo:
    id: int
    name: str


@dataclass
class SenderInfo:
    id: int
    name: str
    username: Optional[str]


@dataclass
class MessageInfo:
    id: int
    date: datetime
    type: str
    text: str
    has_media: bool
    file_path: Optional[Path]


@dataclass
class TelegramMessage:

    chat: ChatInfo

    sender: SenderInfo

    message: MessageInfo