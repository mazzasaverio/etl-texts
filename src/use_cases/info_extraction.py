import os
import json
import openai
from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

# Load environment variables
load_dotenv()
source_path = os.getenv("PATH_SOURCE_INFO_EXTRACTION")
destination_path = os.getenv("PATH_DESTINATION_INFO_EXTRACTION")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ensure OpenAI API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key not set in .env file")


client = OpenAI()


def analyze_text_with_gpt3(text):
    prompt_role_user = os.getenv("PROMPT_ROLE_USER")
    prompt_role_system = os.getenv("PROMPT_ROLE_SYSTEM")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt_role_system,
                },
                {
                    "role": "user",
                    "content": f"This text is extracted from a document: '{text[:600]}'. {prompt_role_user}",
                },
            ],
            max_tokens=130,
        )
        response_text = completion.choices[0].message

        response_text_content = response_text.content

        response_text_content_json = json.loads(response_text_content)
        return response_text_content_json
    except Exception as e:
        logger.error(f"Error in GPT-3.5 analysis: {e}")
        return "Error in GPT-3.5 analysis"


def process_file(file_name):
    file_path = os.path.join(source_path, file_name)
    with open(file_path, "r") as file:
        data = json.load(file)

    analysis_result = analyze_text_with_gpt3(data["tot_text_cleaned"])

    # Save the updated data in the destination path
    dest_file_path = os.path.join(destination_path, file_name)
    with open(dest_file_path, "w") as file:
        json.dump(analysis_result, file, indent=4)
        logger.info(f"Processed and saved: {dest_file_path}")


def file_already_processed(file_name):
    processed_files = os.listdir(destination_path)
    return file_name in processed_files


def main():
    for file_name in os.listdir(source_path):
        if file_name.endswith(".json") and not file_already_processed(file_name):
            logger.info(f"Processing file: {file_name}")
            process_file(file_name)
        else:
            logger.info(f"Skipping already processed file: {file_name}")


if __name__ == "__main__":
    main()
