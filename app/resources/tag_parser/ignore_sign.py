import re
import typing

from interfaces.resources.tag_parser import TagParser


class TagParserWithIgnoreSign(TagParser):

    def parse(self, message_text: str) -> typing.List[str]:
        pattern = '#?[\w\d]+'
        sub_strings = re.findall(fr'{pattern}', message_text)
        return [item.replace('#', '').lower() for item in sub_strings]
