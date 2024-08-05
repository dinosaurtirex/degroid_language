from source.languages.russian.language import RussianLanguage


def main():
    result = RussianLanguage("Привет!")()
    print(result)


if __name__ == "__main__":
    main()