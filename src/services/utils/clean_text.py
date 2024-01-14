import re
from bs4 import BeautifulSoup


def clean_text_type1(text):
    """
    Cleans input text for embedding and classification.

    Steps:
    1. HTML decoding: Converts HTML entities to their corresponding characters.
    2. Lowercasing: Converts all characters to lowercase for uniformity.
    3. Removing URLs: Deletes any web addresses.
    4. Removing special characters: Strips out symbols and punctuation.
    5. Removing extra whitespaces: Collapses multiple spaces into one.
    6. Optional: Advanced processing like stemming/lemmatization, removing stop words, etc.

    :param text: str - The input text to be cleaned.
    :return: str - The cleaned text.
    """

    # HTML decoding
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # Lowercasing
    text = text.lower()

    # Removing URLs
    text = re.sub(r"http\S+", "", text)

    # Removing special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Removing extra whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    # Optional: Add additional text processing steps here if required

    return text
