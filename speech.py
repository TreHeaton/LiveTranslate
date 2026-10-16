
from faster_whisper import WhisperModel

# Smaller model for faster CPU transcription
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_file):
    print("Transcribing audio locally...")

    segments, info = model.transcribe(
        audio_file,
        beam_size=1
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()
