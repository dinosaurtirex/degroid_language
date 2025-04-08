from abc import ABC, abstractmethod
from typing import List

class TextReader(ABC):
    """Abstract base class for reading text from different sources."""
    
    @abstractmethod
    def read_text(self) -> str:
        """Read and return the entire text content."""
        pass
    
    @abstractmethod
    def read_lines(self) -> List[str]:
        """Read and return text as a list of lines."""
        pass
    
    @abstractmethod
    def read_chunk(self, chunk_size: int) -> str:
        """Read a specific chunk of text."""
        pass
    
    @abstractmethod
    def read_range(self, start: int, end: int) -> str:
        """Read text within a specific range."""
        pass
    
    @abstractmethod
    def get_file_size(self) -> int:
        """Get the size of the text source in bytes."""
        pass
    
    @abstractmethod
    def get_encoding(self) -> str:
        """Get the encoding of the text source."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the text source and release resources."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 