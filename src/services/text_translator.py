import os
import json
from dotenv import load_dotenv
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from loguru import logger
from tqdm import tqdm

# Load environment variables
load_dotenv()
source_path = os.getenv("PATH_SOURCE_TEXT_TRANSLATION")
destination_path = os.getenv("PATH_DESTINATION_TEXT_TRANSLATION")
target_language = os.getenv("TARGET_LANGUAGE_TRANSLATION")


# Check if the paths and target language are set
if not source_path:
    raise ValueError("Translation source path not set in .env file")
if not destination_path:
    raise ValueError("Translation destination path not set in .env file")
if not target_language:
    raise ValueError("Target language not set in .env file")

# Initialize translator
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# from langdetect import detect


def translate_text(text, source_language, target_language):
    """Translate text from source language to the target language."""

    # try:
    #     # logger.info(f"{source_language} - {target_language}")
    #     source_language = detect(text)
    #     # logger.info(f"Detected language {text}: {source_language}")
    # except:
    #     logger.error(f"Could not detect language for text: {text}")
    #     return text

    language_code_map = {
        "nld": "nl",  # Dutch
        "eng": "en",  # English
        "fra": "fr",  # French
        "deu": "de",  # German
        "ita": "it",  # Italian
    }

    source_language = language_code_map.get(source_language, source_language)
    # logger.info(
    #     f"Source language: {source_language} - Target language: {target_language}"
    # )

    if source_language == target_language:
        return text  # Skip translation if languages are the same

    try:
        tokenizer.src_lang = source_language
        encoded = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded, forced_bos_token_id=tokenizer.get_lang_id(target_language)
        )
        translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        logger.info(
            f"Translating from {source_language} to {target_language} -  TEXT: {text} - TRANSLATION: {translation[0]}"
        )
        return translation[0]
    except Exception as e:
        logger.error(
            f"Error in translation from {source_language} to {target_language}: {e}"
        )
        return text


def process_files(source_dir, dest_dir, target_lang):
    """Process each JSON file in the source directory."""
    for file in tqdm(os.listdir(source_dir)):
        # logger.info(f"Processing file {file}")
        if file.endswith(".json") and not translation_exists(file, dest_dir):
            file_path = os.path.join(source_dir, file)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                translate_and_save(data, file, dest_dir, target_lang)


def translate_and_save(data, file_name, dest_dir, target_lang):
    """Translate text in data and save to a new JSON file in the destination directory."""

    translated_elements = []
    for element in data:
        source_language = element["metadata"]["languages"][
            0
        ]  # Assuming first language is source
        translated_text = translate_text(element["text"], source_language, target_lang)
        translated_elements.append(
            {
                "element_id": element["element_id"],
                "filename": element["metadata"]["filename"],
                "type": element["type"],
                "text": element["text"],
                "source_language": source_language,
                "text_translated": translated_text,
                "target_lang": target_lang,
            }
        )

    new_file_path = os.path.join(
        dest_dir, file_name.replace(".json", "_translated.json")
    )
    with open(new_file_path, "w") as json_file:
        json.dump(translated_elements, json_file, ensure_ascii=False, indent=4)


def translation_exists(file_name, dest_dir):
    """Check if a translated version of the file already exists in the destination directory."""
    translated_file_name = file_name.replace(".json", "_translated.json")
    return translated_file_name in os.listdir(dest_dir)


if __name__ == "__main__":
    process_files(source_path, destination_path, target_language)
