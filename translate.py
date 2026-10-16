from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


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


print("Loading translation model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    src_lang=SOURCE_LANGUAGE
)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def translate_text(text, target_language_code):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(
            target_language_code
        ),
        max_new_tokens=128
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text

