from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


MODEL_NAME = "facebook/nllb-200-distilled-600M"

SOURCE_LANGUAGE = "eng_Latn"
TARGET_LANGUAGE = "jpn_Jpan"


print("Loading translation model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    src_lang=SOURCE_LANGUAGE
)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def translate_to_japanese(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(
            TARGET_LANGUAGE
        ),
        max_new_tokens=128
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text


