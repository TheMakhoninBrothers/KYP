import typing
from abc import ABC, abstractmethod


class TagParser(ABC):
    """Interface of tag parser"""

    @abstractmethod
    def parse(self, message_text: str) -> typing.List[str]:
        """Parse tag from message text."""
