import argparse
from source.languages.russian.language import RussianLanguage
from source.core.text_reader import TxtFileReader
from source.core.clipboard import get_clipboard_manager


def main():
    parser = argparse.ArgumentParser(description='Process Russian text using Degroid Language')
    parser.add_argument('text', nargs='?', help='Text to process (if not provided, will use default)')
    parser.add_argument('--file', '-f', help='Path to text file to process')
    parser.add_argument('--copy', '-c', action='store_true', help='Copy result to clipboard')
    args = parser.parse_args()
    if args.file:
        text = TxtFileReader(args.file).read_text()
    else:
        text = args.text if args.text else "Привет!"
    result = RussianLanguage(text)()
    if args.copy:
        clipboard = get_clipboard_manager()
        clipboard.get_writer().write_text(result)
        print("Result copied to clipboard!")


if __name__ == "__main__":
    main()