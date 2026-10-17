
import os

# Configure CPU threading before importing PyTorch
os.environ.setdefault("OMP_NUM_THREADS", "4")

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# ==========================================
# LiveTranslate v0.6
# Optimized CPU Translation
# ==========================================

MODEL_NAME = "facebook/nllb-200-distilled-600M"

SOURCE_LANGUAGE = "eng_Latn"

LANGUAGES = {
    "1": {
        "name": "Japanese",
        "code": "jpn_Jpan"
    },
    "2": {
        "name": "Spanish",
        "code": "spa_Latn"
    },
    "3": {
        "name": "French",
        "code": "fra_Latn"
    },
    "4": {
        "name": "German",
        "code": "deu_Latn"
    },
    "5": {
        "name": "Korean",
        "code": "kor_Hang"
    }
}


# Use four CPU threads as an initial benchmark
torch.set_num_threads(4)

print("Loading translation model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    src_lang=SOURCE_LANGUAGE
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

# Put the model in inference mode
model.eval()

print("Translation model ready.")


@torch.inference_mode()
def translate_text(text, target_language_code):
    """Translate English text using the NLLB model."""

    if not text or not text.strip():
        return ""

    # Convert input text into model tokens
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True
    )

    # Identify the requested output language
    language_token_id = tokenizer.convert_tokens_to_ids(
        target_language_code
    )

    # Generate the translation
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=language_token_id,
        max_new_tokens=64,
        num_beams=1,
        do_sample=False
    )

    # Convert tokens back into readable text
    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text
