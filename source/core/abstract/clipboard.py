from abc import ABC, abstractmethod
from typing import Optional, Union
from enum import Enum, auto


class ClipboardFormat(Enum):
    """Supported clipboard formats."""
    TEXT = auto()
    HTML = auto()
    RTF = auto()
    IMAGE = auto()


class ClipboardReader(ABC):
    """Abstract base class for reading from clipboard."""
    
    @abstractmethod
    def read_text(self) -> str:
        """Read text from clipboard."""
        pass
    
    @abstractmethod
    def read_html(self) -> str:
        """Read HTML from clipboard."""
        pass
    
    @abstractmethod
    def read_rtf(self) -> str:
        """Read RTF from clipboard."""
        pass
    
    @abstractmethod
    def has_format(self, format: ClipboardFormat) -> bool:
        """Check if clipboard has specific format."""
        pass


class ClipboardWriter(ABC):
    """Abstract base class for writing to clipboard."""
    
    @abstractmethod
    def write_text(self, text: str) -> None:
        """Write text to clipboard."""
        pass
    
    @abstractmethod
    def write_html(self, html: str) -> None:
        """Write HTML to clipboard."""
        pass
    
    @abstractmethod
    def write_rtf(self, rtf: str) -> None:
        """Write RTF to clipboard."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear clipboard contents."""
        pass


class ClipboardManager(ABC):
    """Abstract base class for clipboard management."""
    
    @abstractmethod
    def get_reader(self) -> ClipboardReader:
        """Get clipboard reader instance."""
        pass
    
    @abstractmethod
    def get_writer(self) -> ClipboardWriter:
        """Get clipboard writer instance."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> list[ClipboardFormat]:
        """Get list of supported clipboard formats for current OS."""
        pass
    
    @abstractmethod
    def is_clipboard_empty(self) -> bool:
        """Check if clipboard is empty."""
        pass
    
    @abstractmethod
    def get_clipboard_history(self, max_items: Optional[int] = None) -> list[str]:
        """Get clipboard history if supported by OS."""
        pass