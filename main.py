from speech import speech_to_text
from translate import translate_text, LANGUAGES


def display_language_menu():
    print()
    print("Select target language:")
    print()

    for number, language in LANGUAGES.items():
        print(f"{number}. {language['name']}")

    print()


def get_language_choice():
    while True:
        choice = input("Enter choice: ")

        if choice in LANGUAGES:
            return LANGUAGES[choice]

        print("Invalid choice. Please select a number from the menu.")


def main():
    print("================================")
    print("       LiveTranslate")
    print("================================")

    display_language_menu()

    selected_language = get_language_choice()

    print()
    print(f"Target language: {selected_language['name']}")

    audio_file = "Testaudiophone.m4a"

    print()

    text = speech_to_text(audio_file)

    print()
    print("Original:")
    print(text)

    translated_text = translate_text(
        text,
        selected_language["code"]
    )

    print()
    print(f"{selected_language['name']}:")
    print(translated_text)


if __name__ == "__main__":
    main()