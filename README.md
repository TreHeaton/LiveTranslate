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

# LiveTranslate

**An offline AI-powered speech recognition and multilingual translation application built with Python.**

LiveTranslate is a personal software development project focused on converting spoken language into translated text. The long-term goal is to develop a real-time translation system that can connect to smart glasses and display subtitles during conversations.

The project currently uses Faster Whisper for speech recognition and Meta's NLLB-200 model for multilingual translation.

## Current Version: v0.2

LiveTranslate currently supports:

- Offline speech recognition using Faster Whisper
- English speech transcription from recorded audio files
- Translation into five languages
- Local AI model inference without paid API calls
- Command-line language selection
- Performance benchmarking for transcription and translation
- CPU inference with quantization for improved efficiency
- Initial NVIDIA CUDA compatibility testing

**Current limitation:** LiveTranslate processes prerecorded audio files. Continuous microphone transcription, real-time subtitles, and smart glasses integration are planned but not yet implemented.

## Supported Languages

| Language | NLLB Language Code |
|---|---|
| Japanese | `jpn_Jpan` |
| Spanish | `spa_Latn` |
| French | `fra_Latn` |
| German | `deu_Latn` |
| Korean | `kor_Hang` |

English is currently the source language for translation.

## Technologies Used

- **Python:** Core application development
- **Faster Whisper:** Speech-to-text transcription
- **CTranslate2:** Optimized inference backend for Faster Whisper
- **Hugging Face Transformers:** Translation model integration
- **Meta NLLB-200 Distilled 600M:** Multilingual neural machine translation
- **PyTorch:** Translation model execution
- **Git and GitHub:** Version control
- **PyCharm:** Development environment

The application uses locally downloaded AI models instead of requiring a paid cloud transcription or translation API.

An internet connection is required for the initial model downloads.

## How LiveTranslate Works

1. The user launches the application.
2. LiveTranslate displays a menu of supported languages.
3. The user selects a target language.
4. Faster Whisper processes a prerecorded audio file and produces an English transcription.
5. NLLB-200 translates the transcription into the selected language.
6. The application displays the original transcription, translated text, and processing times.

### Project Structure

```text
LiveTranslate/
├── main.py
├── speech.py
├── translate.py
├── audio.py
├── requirements.txt
├── README.md
└── .gitignore
```

**main.py:** Controls the application workflow, language selection, and performance measurements.

**speech.py:** Handles local speech recognition using Faster Whisper.

**translate.py:** Loads the NLLB translation model and translates text into the selected language.

**audio.py:** Contains experimental audio-recording functionality for future microphone support.

## Installation and Setup

### Prerequisites

- Python and pip
- Git (optional)
- Sufficient storage for downloaded AI models
- Windows, Linux, or macOS with compatible dependencies

This project is currently developed and tested on Windows using Python 3.14.7. Compatibility with other environments has not yet been fully verified.

### Clone the Repository

```bash
git clone https://github.com/TreHeaton/LiveTranslate.git
cd LiveTranslate
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The dependency file should be kept synchronized with the packages installed in the development environment.

### Provide Test Audio

Place a supported audio recording in the project directory.

The current `main.py` expects an audio file named:

```text
Testaudiophone.m4a
```

You can modify the `audio_file` variable in `main.py` to use another filename.

Test audio is excluded from version control.

### Run LiveTranslate

```bash
python main.py
```

Select a language from the displayed menu.

The application will transcribe the recording, translate the text, and display the results.

## Performance Optimization

During v0.2 development, performance measurements were added to identify bottlenecks in the speech recognition and translation pipeline.

### Benchmark Results

Testing was performed on a desktop computer with:

- AMD Ryzen 5 2400G, 4 cores and 8 threads
- NVIDIA GeForce GTX 1660, 6 GB VRAM
- Windows and Python 3.14.7

| Component | Initial CPU Test | Optimized CPU Test |
|---|---:|---:|
| Speech recognition | 10.78 seconds | 3.04 seconds |
| Translation | 16.48 seconds | 3.48 seconds |
| Total processing | 27.25 seconds | 6.52 seconds |

**Observed improvement:** Approximately 76% reduction in total processing time between the two tests.

Changes to speech recognition included:

- Switching from Whisper `small` to `base`
- Using INT8 CPU inference
- Setting beam size to 1

The translation model remained unchanged between these tests. Its observed speed improvement may reflect system load, warm-up effects, or other runtime differences.

These are preliminary single-run benchmarks, not controlled averages. Model loading and application startup are excluded from the processing measurements.

Smaller models and simpler decoding can improve performance but may reduce transcription accuracy.

## GPU Acceleration: In Progress

The project is being evaluated for NVIDIA CUDA acceleration using a GTX 1660.

Initial tests confirmed that:

- The NVIDIA GPU is detected by CTranslate2.
- Faster Whisper can load a model configured for CUDA.
- Actual GPU transcription requires additional CUDA runtime dependencies.

GPU inference has not yet been successfully benchmarked.

The working implementation currently uses CPU inference.

## Development Roadmap

### v0.1: Initial Prototype
- [x] Implement local speech recognition
- [x] Integrate NLLB-200 translation
- [x] Translate recorded English speech into Japanese
- [x] Configure local model caching
- [x] Create GitHub repository

### v0.2: Multilingual Support and Optimization
- [x] Add five target languages
- [x] Implement command-line language selection
- [x] Add transcription and translation timing
- [x] Test smaller Whisper models
- [x] Benchmark CPU performance
- [ ] Complete GPU acceleration testing
- [ ] Add automated tests and error handling

### v0.3: Continuous Audio Processing
- [ ] Add microphone input
- [ ] Process shorter audio segments
- [ ] Support continuous transcription
- [ ] Reduce end-to-end translation latency

### v0.4: Backend API
- [ ] Create an API for transcription and translation
- [ ] Add structured requests and responses
- [ ] Investigate streaming communication

### v0.5: User Interface
- [ ] Develop a web interface
- [ ] Display original and translated subtitles
- [ ] Add language selection controls

### v0.6 and Beyond: Mobile and Wearable Integration
- [ ] Investigate Android application development
- [ ] Connect mobile microphone input
- [ ] Explore compatible smart glasses
- [ ] Display translated subtitles on wearable devices

## Potential Applications

LiveTranslate is being developed with several possible applications in mind:

- Travel and international communication
- Language learning
- Accessibility and translated captions
- Multilingual customer support
- Healthcare communication assistance

Healthcare use would require substantial additional work involving translation accuracy, privacy, reliability, and appropriate human oversight. This prototype is not intended to replace qualified medical interpreters or support safety-critical clinical decisions.

## What I've Learned

Developing LiveTranslate has provided practical experience with:

- Building modular Python applications
- Integrating open-source machine learning models
- Running AI inference locally
- Managing Python virtual environments and dependencies
- Troubleshooting API limitations and library compatibility
- Configuring model storage and caching
- Using Git and GitHub for version control
- Measuring software performance
- Evaluating CPU and GPU acceleration
- Balancing speed, accuracy, and resource requirements

## Future Goals

The long-term objective is to turn LiveTranslate into a practical, low-latency translation application that can display translated subtitles during conversations.

Future development will focus on real-time audio processing, application architecture, user interfaces, mobile compatibility, and smart glasses integration.

## Author

**Tre Heaton**

Computer Science Student | Software Engineering

GitHub: https://github.com/TreHeaton

## Project Status

**Active Development | Version 0.2**

LiveTranslate is an educational and portfolio project. Features, performance, and supported platforms may change as development continues.
