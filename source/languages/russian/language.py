from source.core.abstract.language import AbstractLanguage
from source.languages.russian.table import RU_CHAR_TABLE


class RussianLanguage(AbstractLanguage):
    def _parse_char(self, char: str) -> str:
        try:
            return RU_CHAR_TABLE[char]
        except KeyError:
            return char