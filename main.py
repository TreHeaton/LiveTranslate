
import time

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
        choice = input("Enter choice: ").strip()

        if choice in LANGUAGES:
            return LANGUAGES[choice]

        print("Invalid choice. Please select a number from the menu.")


def main():
    print("================================")
    print("       LiveTranslate v0.2")
    print("================================")

    # Display available languages
    display_language_menu()

    # Get the user's selected language
    selected_language = get_language_choice()

    print()
    print(f"Target language: {selected_language['name']}")

    # Audio file used for testing
    audio_file = "Testaudiophone.m4a"

    print()

    # Start speech recognition timer
    speech_start = time.perf_counter()

    # Convert recorded speech into English text
    text = speech_to_text(audio_file)

    # Calculate speech recognition time
    speech_time = time.perf_counter() - speech_start

    print()
    print("Original:")
    print(text)

    # Start translation timer
    translation_start = time.perf_counter()

    # Translate the English text into the selected language
    translated_text = translate_text(
        text,
        selected_language["code"]
    )

    # Calculate translation time
    translation_time = time.perf_counter() - translation_start

    print()
    print(f"{selected_language['name']}:")
    print(translated_text)

    # Display performance results
    total_time = speech_time + translation_time

    print()
    print("================================")
    print("       Performance Results")
    print("================================")
    print(f"Speech recognition: {speech_time:.2f} seconds")
    print(f"Translation:        {translation_time:.2f} seconds")
    print(f"Total processing:   {total_time:.2f} seconds")
    print("================================")


if __name__ == "__main__":
    main()
