from typing import List
from pathlib import Path
from source.core.abstract.text_reader import TextReader


class TxtFileReader(TextReader):
    """Concrete implementation of TextReader for reading .txt files."""
    
    def __init__(self, file_path: str | Path, encoding: str = 'utf-8'):
        """
        Initialize the TxtFileReader.
        
        Args:
            file_path: Path to the .txt file
            encoding: File encoding (default: utf-8)
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._file = None
        self._open_file()
    
    def _open_file(self) -> None:
        """Open the file if it's not already open."""
        if self._file is None:
            self._file = open(self.file_path, 'r', encoding=self.encoding)
    
    def read_text(self) -> str:
        """Read and return the entire text content."""
        self._open_file()
        return self._file.read()
    
    def read_lines(self) -> List[str]:
        """Read and return text as a list of lines."""
        self._open_file()
        return self._file.readlines()
    
    def read_chunk(self, chunk_size: int) -> str:
        """Read a specific chunk of text."""
        self._open_file()
        return self._file.read(chunk_size)
    
    def read_range(self, start: int, end: int) -> str:
        """Read text within a specific range."""
        self._open_file()
        self._file.seek(start)
        return self._file.read(end - start)
    
    def get_file_size(self) -> int:
        """Get the size of the text source in bytes."""
        return self.file_path.stat().st_size
    
    def get_encoding(self) -> str:
        """Get the encoding of the text source."""
        return self.encoding
    
    def close(self) -> None:
        """Close the text source and release resources."""
        if self._file is not None:
            self._file.close()
            self._file = None 