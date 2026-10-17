
import sounddevice as sd
from scipy.io.wavfile import write

DEVICE_ID = 1
SAMPLE_RATE = 16000
DURATION = 5

print("LiveTranslate Microphone Test")
print("=============================")
print("Recording starts now. Speak into your headset!")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=DEVICE_ID
)

sd.wait()

write("microphone_test.wav", SAMPLE_RATE, audio)

print("Recording complete!")
print("Saved as microphone_test.wav")
