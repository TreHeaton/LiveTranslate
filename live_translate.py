
import queue
import threading
import time
from collections import deque

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from speech import speech_to_text
from translate import translate_text


# ==========================================
# LiveTranslate v0.5
# Low-Latency Translation
# ==========================================

# Microphone settings
DEVICE_ID = 1
SAMPLE_RATE = 16000
BLOCK_DURATION = 0.1

# Silence detection settings
SILENCE_THRESHOLD = 0.015
SILENCE_DURATION = 0.5
MIN_SPEECH_DURATION = 0.4
MAX_SEGMENT_DURATION = 10.0
PRE_ROLL_DURATION = 0.3

# Processing queue
audio_queue = queue.Queue(maxsize=10)
stop_event = threading.Event()

# Supported translation languages
LANGUAGES = {
    "1": ("Japanese", "jpn_Jpan"),
    "2": ("Spanish", "spa_Latn"),
    "3": ("French", "fra_Latn"),
    "4": ("German", "deu_Latn"),
    "5": ("Korean", "kor_Hang")
}


def select_language():
    """Allow the user to select a target language."""

    print("\nSelect target language:\n")

    for number, (name, code) in LANGUAGES.items():
        print(f"{number}. {name}")

    while True:
        choice = input("\nEnter choice: ").strip()

        if choice in LANGUAGES:
            return LANGUAGES[choice]

        print("Invalid choice. Try again.")


def get_audio_level(audio):
    """Calculate normalized microphone volume."""

    samples = audio.astype(np.float32) / 32768.0

    return float(np.sqrt(np.mean(samples ** 2)))


def queue_segment(blocks, speech_blocks):
    """Add a completed speech segment to the queue."""

    if speech_blocks * BLOCK_DURATION < MIN_SPEECH_DURATION:
        return

    audio = np.concatenate(blocks)

    try:
        # Store audio and capture timestamp together
        audio_queue.put_nowait(
            (audio, time.perf_counter())
        )

        print("[Speech segment captured]")

    except queue.Full:
        print("[Queue full: segment skipped]")


def record_audio():
    """Continuously listen and group speech by pauses."""

    block_size = int(SAMPLE_RATE * BLOCK_DURATION)

    silence_blocks_needed = int(
        SILENCE_DURATION / BLOCK_DURATION
    )

    max_blocks = int(
        MAX_SEGMENT_DURATION / BLOCK_DURATION
    )

    pre_roll_blocks = max(
        1,
        int(PRE_ROLL_DURATION / BLOCK_DURATION)
    )

    pre_roll = deque(maxlen=pre_roll_blocks)

    recording = False
    speech_blocks = 0
    silence_blocks = 0
    segment_blocks = []

    print("\nMicrophone started.")
    print("Speak normally and pause between sentences.")
    print("Press Ctrl+C to stop.\n")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            device=DEVICE_ID,
            blocksize=block_size
        ) as stream:

            while not stop_event.is_set():

                audio, overflowed = stream.read(block_size)

                if overflowed:
                    print("[Microphone input overflow]")

                block = audio.copy().flatten()

                level = get_audio_level(block)

                speaking = level > SILENCE_THRESHOLD

                if not recording:

                    pre_roll.append(block)

                    if speaking:
                        recording = True

                        segment_blocks = list(pre_roll)

                        speech_blocks = 1
                        silence_blocks = 0

                        pre_roll.clear()

                        print("[Speech detected]")

                else:

                    segment_blocks.append(block)

                    if speaking:
                        speech_blocks += 1
                        silence_blocks = 0

                    else:
                        silence_blocks += 1

                    # Finish segment after silence
                    # or maximum recording duration
                    if (
                        silence_blocks >= silence_blocks_needed
                        or len(segment_blocks) >= max_blocks
                    ):

                        queue_segment(
                            segment_blocks,
                            speech_blocks
                        )

                        recording = False
                        segment_blocks = []
                        speech_blocks = 0
                        silence_blocks = 0

            # Save remaining speech when stopping
            if recording:
                queue_segment(
                    segment_blocks,
                    speech_blocks
                )

    except Exception as error:
        print(f"Microphone error: {error}")
        stop_event.set()


def process_audio(target_language, language_name):
    """Transcribe, translate, and measure processing time."""

    segment_number = 0

    while not stop_event.is_set() or not audio_queue.empty():

        try:
            audio, captured_at = audio_queue.get(
                timeout=0.3
            )

        except queue.Empty:
            continue

        segment_number += 1

        try:
            start = time.perf_counter()

            # Save the audio segment
            filename = "current_segment.wav"

            write(
                filename,
                SAMPLE_RATE,
                audio
            )

            # ==================================
            # Speech recognition using GPU
            # ==================================

            original_text = speech_to_text(filename)

            transcription_time = (
                time.perf_counter() - start
            )

            if not original_text.strip():
                print("[No speech detected]")
                continue

            # ==================================
            # Translation using NLLB
            # ==================================

            translation_start = time.perf_counter()

            translated_text = translate_text(
                original_text,
                target_language
            )

            translation_time = (
                time.perf_counter() - translation_start
            )

            # ==================================
            # Total processing measurements
            # ==================================

            elapsed = time.perf_counter() - start

            total_delay = (
                time.perf_counter() - captured_at
            )

            # ==================================
            # Display results
            # ==================================

            print("\n================================")
            print(f"Segment {segment_number}")
            print("================================")

            print(f"English: {original_text}")
            print(f"{language_name}: {translated_text}")

            print("\nPerformance:")
            print(f"Whisper + WAV: {transcription_time:.2f} seconds")
            print(f"NLLB: {translation_time:.2f} seconds")
            print(f"Processing: {elapsed:.2f} seconds")
            print(f"Delay after capture: {total_delay:.2f} seconds")

            print("================================\n")

        except Exception as error:
            print(f"Processing error: {error}")

        finally:
            audio_queue.task_done()


def main():
    """Start LiveTranslate."""

    print("================================")
    print("       LiveTranslate v0.5")
    print("       Low-Latency Translation")
    print("================================")

    language_name, language_code = select_language()

    print(f"\nTarget language: {language_name}")

    recorder = threading.Thread(
        target=record_audio,
        daemon=True
    )

    recorder.start()

    try:
        process_audio(
            language_code,
            language_name
        )

    except KeyboardInterrupt:
        print("\nStopping LiveTranslate...")

    finally:
        stop_event.set()

        recorder.join(timeout=2)

        print("LiveTranslate stopped.")


if __name__ == "__main__":
    main()
