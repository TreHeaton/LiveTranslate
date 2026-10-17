
from faster_whisper import WhisperModel

# Load Faster Whisper using NVIDIA GPU acceleration
model = WhisperModel(
    "base",
    device="cuda",
    compute_type="float16"
)


def speech_to_text(audio_file):
    print("Transcribing audio using NVIDIA GPU...")

    segments, info = model.transcribe(
        audio_file,
        beam_size=1
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()
