from faster_whisper import WhisperModel


# Load the speech recognition model.
# "small" provides a good balance between accuracy and performance.
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_file):
    print("Transcribing audio locally...")

    segments, info = model.transcribe(audio_file)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()