import platform
from typing import Optional, List
import ctypes
from ctypes import wintypes
from source.core.abstract.clipboard import (
    ClipboardManager,
    ClipboardReader,
    ClipboardWriter,
    ClipboardFormat
)

CF_TEXT = 1
CF_UNICODETEXT = 13
CF_HTML = 49409
CF_RTF = 49513

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.OpenClipboard.restype = wintypes.BOOL

user32.CloseClipboard.argtypes = []
user32.CloseClipboard.restype = wintypes.BOOL

user32.EmptyClipboard.argtypes = []
user32.EmptyClipboard.restype = wintypes.BOOL

user32.IsClipboardFormatAvailable.argtypes = [wintypes.UINT]
user32.IsClipboardFormatAvailable.restype = wintypes.BOOL

user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.GetClipboardData.restype = wintypes.HANDLE

user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
user32.SetClipboardData.restype = wintypes.HANDLE

kernel32.GlobalLock.argtypes = [wintypes.HANDLE]
kernel32.GlobalLock.restype = wintypes.LPVOID

kernel32.GlobalUnlock.argtypes = [wintypes.HANDLE]
kernel32.GlobalUnlock.restype = wintypes.BOOL

kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = wintypes.HANDLE

kernel32.GlobalSize.argtypes = [wintypes.HANDLE]
kernel32.GlobalSize.restype = ctypes.c_size_t

kernel32.lstrcpy.argtypes = [wintypes.LPVOID, wintypes.LPCVOID]
kernel32.lstrcpy.restype = wintypes.LPVOID

kernel32.lstrlen.argtypes = [wintypes.LPCVOID]
kernel32.lstrlen.restype = wintypes.INT


class WindowsClipboardReader(ClipboardReader):
    """Windows implementation of clipboard reader using WinAPI."""
    
    def _get_clipboard_text(self, format_id: int) -> str:
        """Get text from clipboard in specified format."""
        if not user32.OpenClipboard(None):
            return ""
        
        try:
            if not user32.IsClipboardFormatAvailable(format_id):
                return ""
            
            handle = user32.GetClipboardData(format_id)
            if not handle:
                return ""
            
            ptr = kernel32.GlobalLock(handle)
            if not ptr:
                return ""
            
            try:
                size = kernel32.GlobalSize(handle)

                buffer = ctypes.create_string_buffer(size)
                kernel32.lstrcpy(buffer, ptr)

                if format_id == CF_UNICODETEXT:
                    return buffer.value.decode('utf-16le').rstrip('\0')
                else:
                    return buffer.value.decode('utf-8').rstrip('\0')
            finally:
                kernel32.GlobalUnlock(handle)
        finally:
            user32.CloseClipboard()
    
    def read_text(self) -> str:
        """Read plain text from clipboard."""
        return self._get_clipboard_text(CF_UNICODETEXT)
    
    def read_html(self) -> str:
        """Read HTML from clipboard."""
        return self._get_clipboard_text(CF_HTML)
    
    def read_rtf(self) -> str:
        """Read RTF from clipboard."""
        return self._get_clipboard_text(CF_RTF)
    
    def has_format(self, format: ClipboardFormat) -> bool:
        """Check if clipboard has specific format."""
        if not user32.OpenClipboard(None):
            return False
        
        try:
            if format == ClipboardFormat.TEXT:
                result = user32.IsClipboardFormatAvailable(CF_UNICODETEXT)
            elif format == ClipboardFormat.HTML:
                result = user32.IsClipboardFormatAvailable(CF_HTML)
            elif format == ClipboardFormat.RTF:
                result = user32.IsClipboardFormatAvailable(CF_RTF)
            else:
                result = False
            return bool(result)
        finally:
            user32.CloseClipboard()


class WindowsClipboardWriter(ClipboardWriter):
    """Windows implementation of clipboard writer using WinAPI."""
    
    def _set_clipboard_text(self, text: str, format_id: int) -> None:
        """Set text to clipboard in specified format."""
        if not user32.OpenClipboard(None):
            return
        
        try:
            user32.EmptyClipboard()

            if format_id == CF_UNICODETEXT:
                data = text.encode('utf-16le') + b'\0\0'
            else:
                data = text.encode('utf-8') + b'\0'

            size = len(data)
            handle = kernel32.GlobalAlloc(0, size)
            if not handle:
                return

            ptr = kernel32.GlobalLock(handle)
            if not ptr:
                kernel32.GlobalFree(handle)
                return
            
            try:
                ctypes.memmove(ptr, data, size)
            finally:
                kernel32.GlobalUnlock(handle)

            user32.SetClipboardData(format_id, handle)
        finally:
            user32.CloseClipboard()
    
    def write_text(self, text: str) -> None:
        """Write plain text to clipboard."""
        self._set_clipboard_text(text, CF_UNICODETEXT)
    
    def write_html(self, html: str) -> None:
        """Write HTML to clipboard."""
        self._set_clipboard_text(html, CF_HTML)
    
    def write_rtf(self, rtf: str) -> None:
        """Write RTF to clipboard."""
        self._set_clipboard_text(rtf, CF_RTF)
    
    def clear(self) -> None:
        """Clear clipboard contents."""
        if user32.OpenClipboard(None):
            try:
                user32.EmptyClipboard()
            finally:
                user32.CloseClipboard()


class WindowsClipboardManager(ClipboardManager):
    """Windows implementation of clipboard manager using WinAPI."""
    
    def __init__(self):
        self._reader = WindowsClipboardReader()
        self._writer = WindowsClipboardWriter()
    
    def get_reader(self) -> ClipboardReader:
        return self._reader
    
    def get_writer(self) -> ClipboardWriter:
        return self._writer
    
    def get_supported_formats(self) -> List[ClipboardFormat]:
        return [
            ClipboardFormat.TEXT,
            ClipboardFormat.HTML,
            ClipboardFormat.RTF
        ]
    
    def is_clipboard_empty(self) -> bool:
        if not user32.OpenClipboard(None):
            return True
        
        try:
            return not user32.IsClipboardFormatAvailable(CF_UNICODETEXT)
        finally:
            user32.CloseClipboard()
    
    def get_clipboard_history(self, max_items: Optional[int] = None) -> List[str]:
        return []


def get_clipboard_manager() -> ClipboardManager:
    """Factory function to get appropriate clipboard manager for current OS."""
    system = platform.system().lower()
    if system == 'windows':
        return WindowsClipboardManager()
    raise NotImplementedError(f"Clipboard manager not implemented for {system}") 