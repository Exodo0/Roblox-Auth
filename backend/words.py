import random

def generate_key(word_list: list, words: int):
    """
    (method) generate_key
    ---------------------
    Generates a key.

    ---

    Parameters
    ```
    word_list : list
        The word list.
    words : int
        The number of words to include in the key.
    ```
    """
    return " ".join(random.choices(word_list, k=words))

def get_words(file: str):
    """
    (method) get_words
    ------------------
    Returns a list of all words in the provided file.

    ---

    Parameters
    ```
    file : str
        File name or directory of the words
    ```
    """
    return [line.strip() for line in open(file, "r")]