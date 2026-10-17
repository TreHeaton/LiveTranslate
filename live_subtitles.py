
import queue
import threading
import time
import tkinter as tk

from scipy.io.wavfile import write

from live_translate import (
    LANGUAGES,
    SAMPLE_RATE,
    audio_queue,
    stop_event,
    record_audio
)
from speech import speech_to_text
from translate import translate_text
from subtitle_window import SubtitleWindow


# Queue for completed subtitle messages
subtitle_queue = queue.Queue()


def process_translations(language_code, language_name):
    """Process microphone audio in the background."""

    segment_number = 0

    while not stop_event.is_set() or not audio_queue.empty():
        try:
            audio, captured_at = audio_queue.get(timeout=0.3)
        except queue.Empty:
            continue

        segment_number += 1

        try:
            start = time.perf_counter()

            filename = "current_segment.wav"
            write(filename, SAMPLE_RATE, audio)

            english = speech_to_text(filename)

            if not english.strip():
                continue

            translated = translate_text(
                english,
                language_code
            )

            elapsed = time.perf_counter() - start

            subtitle_queue.put((
                english,
                translated,
                language_name,
                elapsed
            ))

            print(f"\nSegment {segment_number}")
            print(f"English: {english}")
            print(f"{language_name}: {translated}")
            print(f"Processing: {elapsed:.2f} seconds")

        except Exception as error:
            print(f"Processing error: {error}")

        finally:
            audio_queue.task_done()


def main():
    print("================================")
    print("       LiveTranslate v0.7")
    print("       Live Subtitle Window")
    print("================================")

    print("\nSelect target language:\n")

    for number, (name, code) in LANGUAGES.items():
        print(f"{number}. {name}")

    while True:
        choice = input("\nEnter choice: ").strip()

        if choice in LANGUAGES:
            break

        print("Invalid choice.")

    language_name, language_code = LANGUAGES[choice]

    # Reset the stop event for this session
    stop_event.clear()

    # Create the Tkinter window on the main thread
    root = tk.Tk()
    app = SubtitleWindow(root)

    app.translation_label.config(
        text=f"TRANSLATED - {language_name.upper()}"
    )
    app.status_label.config(text="Listening...")

    # Start microphone recording
    recorder = threading.Thread(
        target=record_audio,
        daemon=True
    )

    # Start transcription and translation
    processor = threading.Thread(
        target=process_translations,
        args=(language_code, language_name),
        daemon=True
    )

    recorder.start()
    processor.start()

    def check_subtitles():
        """Transfer completed subtitles to the Tkinter UI."""

        while True:
            try:
                english, translated, language, elapsed = (
                    subtitle_queue.get_nowait()
                )
            except queue.Empty:
                break

            app.update_subtitles(
                english,
                translated,
                language
            )

            app.status_label.config(
                text=f"Translated in {elapsed:.2f} seconds"
            )

            subtitle_queue.task_done()

        root.after(100, check_subtitles)

    def on_close():
        """Stop recording when the window closes."""

        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start checking for new subtitles
    root.after(100, check_subtitles)

    try:
        root.mainloop()
    finally:
        stop_event.set()
        recorder.join(timeout=2)
        processor.join(timeout=2)

    print("LiveTranslate stopped.")


if __name__ == "__main__":
    main()
