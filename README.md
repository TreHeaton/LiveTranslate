LiveTranslate
Offline speech recognition and multilingual subtitles, built with Python.
LiveTranslate is a personal software engineering project that listens to spoken English, transcribes it locally, translates the recognized text into a selected language, and displays the latest English and translated subtitles in a desktop window.
The project is currently a Windows desktop prototype (v0.7). Android support and smart-glasses integration are planned, not yet implemented.
Features
- Continuous microphone listening with energy-based silence detection and speech segmentation
- Local English speech recognition using Faster-Whisper with NVIDIA GPU acceleration
- Local machine translation using Meta's NLLB-200 distilled 600M model
- Five translation targets: Japanese, Spanish, French, German, and Korean
- Live subtitle window built with Tkinter, displaying the latest recognized English text and its translation
- Background processing using threads and queues to keep microphone capture and the user interface responsive
- Performance measurements for transcription, translation, and processing delay in the terminal-based workflow
- No paid translation or speech API required; models can run locally after their initial download
How it works
Microphone (English speech)
          |
          v
Energy-based silence detection
          |
          v
Audio segment queue
          |
          v
Faster-Whisper (NVIDIA GPU)
          |
          v
English transcription
          |
          v
NLLB-200 translation (CPU)
          |
          v
Subtitle queue
          |
          v
Tkinter window: English + translated text
The current implementation updates subtitles sentence by sentence after a pause, rather than word by word. Latency varies with sentence length and hardware.
Tech stack
- Python
- Faster-Whisper / CTranslate2
- Hugging Face Transformers and PyTorch
- facebook/nllb-200-distilled-600M
- NumPy, SoundDevice, SciPy
- Tkinter
- Threading and thread-safe queues
Getting started
Requirements
- Windows computer with a working microphone
- Python and a virtual environment
- Dependencies listed in requirements.txt
- NVIDIA GPU and compatible CUDA/cuDNN runtime for the current GPU-configured speech.py
- Internet access for the initial model downloads; subsequent inference can run locally with cached models
Hardware note: The current code uses a configured microphone device ID and initializes Faster-Whisper on CUDA. You may need to adjust DEVICE_ID in live_translate.py and the model/device settings in speech.py for your own computer.

Install
From the project directory in PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Model downloads may take time on the first run. Make sure your CUDA and cuDNN libraries are correctly installed and available if using the current GPU configuration.
Run the live subtitle application
python live_subtitles.py
1. Choose a target language by entering a number from 1 to 5 in the terminal.
2. Wait for the subtitle window and microphone to start.
3. Speak English and pause briefly between sentences.
4. Read the original text and translated subtitle in the window.
5. Close the window to stop the session.
Run the terminal-only translator
python live_translate.py
This version also prints separate speech recognition and translation timings.
Preview the subtitle window without a microphone
python subtitle_window.py
This launches a demo with sample text, not live audio.
Project files
File	Purpose
live_subtitles.py	Connects microphone capture, transcription, translation, and the live subtitle window
subtitle_window.py	Tkinter subtitle interface and standalone UI demo
live_translate.py	Continuous microphone recording, silence detection, and terminal-based translation
speech.py	English speech recognition using Faster-Whisper
translate.py	NLLB translation into the selected language
microphone.py	Microphone testing utility
main.py	Earlier audio-file translation workflow


Development progress
Version	Milestone	Status
v0.1–v0.3	Local speech recognition and translation; continuous microphone prototype	Complete
v0.4	Silence-based speech segmentation	Complete
v0.5	Processing and queue-delay measurements	Complete
v0.6	CPU translation inference adjustments	Complete
v0.7	Live desktop subtitle window	Complete
v0.8	Android application prototype	Planned
Future	Compatible smart-glasses subtitle output	Planned


Known limitations
- The current application is a desktop prototype, not an Android app.
- The default microphone device ID is machine-specific.
- GPU speech recognition requires compatible NVIDIA/CUDA/cuDNN setup as currently configured.
- Speech segmentation uses audio volume thresholds and can split sentences or react to background noise.
- Subtitles appear after a completed speech segment and processing delay; they are not word-level streaming captions.
- Translation accuracy varies with language, phrasing, and speech recognition quality.
- The subtitle window currently displays the latest translated segment rather than a full conversation history.
Roadmap
- Build an Android UI with language selection, microphone controls, and subtitles
- Evaluate smaller, mobile-compatible offline speech and translation models
- Improve segmentation, subtitle timing, and translation accuracy
- Explore supported display-glasses connections for wearable subtitles
Motivation
LiveTranslate is an independent learning and portfolio project focused on practical AI integration, concurrency, performance measurement, and accessible multilingual communication. The long-term goal is to make translated speech easier to follow on mobile devices and, eventually, compatible wearable displays.
License
No license has been specified yet. Check the repository for any future licensing information. Third-party models and libraries are subject to their respective licenses and terms.