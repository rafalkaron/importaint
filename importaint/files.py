# coding utf-8
__author__ = "Rafał Karoń <rafalkaron@gmail.com>"

import requests

def read_file(filepath):
    """Return a string with file contents."""
    with open(filepath, mode='rt', encoding='utf-8') as f:
        return f.read()

def read_external_file(url):
    """Return a string with external file contents."""
    res = requests.get(url)
    return res.text

def save_str_as_file(string, filepath):
    """Save a string to a file and return the file path."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(string)
    return filepath