# coding utf-8
"""
Merge a CSS file with imports into a single file.
"""

import sys
import os
import glob
import re
import argparse

__author__ = "Rafał Karoń <rafalkaron@gmail.com>"
__version__ = "0.2"

def files_list(directory, files_extension):
    """Return a list of files with a given extension in a directory."""
    files_list_lowercase = glob.glob(f"{directory}/*.{files_extension.lower()}")
    files_list_uppercase = glob.glob(f"{directory}/*.{files_extension.upper()}")
    files_list = files_list_lowercase + files_list_uppercase
    return files_list

def read_file(filepath):
    """Return a string with file contents."""
    with open(filepath, mode='rt', encoding='utf-8') as f:
        return f.read()

def get_imports(filepath):
    input_str = read_file(filepath)
    imports = re.findall(r"@import url\(\"(.*.css)\"\);", input_str)
    return imports

def append_str(str_list, output_filepath):
    """Appends a string or a list of strings to a file and return the file path."""
    if type(str_list) is list:    
        print(f"Appended the following files to {output_filepath}:")
        for item in str_list:
            try:
                item_str = read_file(item)
                print(f" [+] {item}")
            except FileNotFoundError:
                print(f" [!] {item} [file does not exist]")
                continue
            with open(output_filepath, "a", encoding="utf-8") as file:
                file.write(f"\n/*!IMPORTAINT; {item} code*/\n{item_str}")
    elif type(str_list) is str:
        with open(output_filepath, "a", encoding="utf-8") as file:
            file.write(str_list)
    return output_filepath

def main():
    par = argparse.ArgumentParser(description="Merge a CSS file with imports into a single file.")
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    par.add_argument("input_filepath", type=str, help="A CSS file with imports.")
    args = par.parse_args()
    
    output_filepath = args.input_filepath.replace(".css", "_compiled.css")
    if os.path.isfile(output_filepath):
        os.remove(output_filepath)
    
    #while len(get_imports(args.input_filepath)) != 0:
    append_str(get_imports(args.input_filepath), output_filepath)

    append_str(f"\n/*!IMPORTAINT; {args.input_filepath} code*/\n", output_filepath)
    input_file_code_str = re.sub(r"@import url\(\"(.*.css)\"\);", "", read_file(args.input_filepath))
    append_str(input_file_code_str, output_filepath)

__main__ = os.path.basename(os.path.abspath(sys.argv[0])).replace(".py","")
if __name__ == "__main__":
    main()