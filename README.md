# LiveTranslate

LiveTranslate is a real-time speech translation project designed to eventually
provide translated subtitles through smart glasses.

## Current Features

- Local speech-to-text using Faster Whisper
- Local machine translation using NLLB-200
- English speech transcription
- English-to-Japanese translation
- Offline AI inference with no paid API required

## Current Pipeline

Audio Input
→ Faster Whisper
→ English Transcription
→ NLLB-200
→ Translated Text

## Project Status

LiveTranslate is currently an early prototype.

### v0.1

The current version can:

1. Read a prerecorded audio file
2. Transcribe speech locally
3. Translate the transcription into Japanese
4. Display the original and translated text

## Planned Features

- Multiple target languages
- Continuous microphone input
- Real-time translation
- Mobile application
- Smart glasses integration
- Speaker isolation
- Subtitle-style display
- OCR and computer vision support

## Technologies

- Python
- Faster Whisper
- Hugging Face Transformers
- NLLB-200
- PyTorch

## Goal

The long-term goal is to create a low-latency translation system capable of
displaying translated conversations as subtitles on wearable smart glasses.