from speech import speech_to_text
from translate import translate_to_japanese


def main():
    print("================================")
    print("       LiveTranslate")
    print("================================")

    audio_file = "Testaudiophone.m4a"

    # Convert the audio recording into English text
    text = speech_to_text(audio_file)

    print()
    print("Original:")
    print(text)

    # Translate the English text into Japanese
    translated_text = translate_to_japanese(text)

    print()
    print("Japanese:")
    print(translated_text)


if __name__ == "__main__":
    main()