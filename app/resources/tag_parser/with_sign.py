import typing

from interfaces.resources.tag_parser import TagParser


class TagParserWithSign(TagParser):

    def parse(self, message_text: str) -> typing.List[str]:
        return [word.replace('#', '').lower() for word in message_text.split(' ') if word.startswith('#')]
