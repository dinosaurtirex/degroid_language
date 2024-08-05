class AbstractLanguage:
    def __init__(self, string):
        self.string = string
        self.parsed_string = None

    def _parse_char(self, char: str):
        raise NotImplementedError("")
    
    def __call__(self) -> str:
        self.parsed_string = "".join(map(self._parse_char, self.string))
        return self.parsed_string
