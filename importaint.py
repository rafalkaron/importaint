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
__version__ = "0.5"

re_imports_filepath = re.compile(r"@import url\(\"(.*.css)\"\);") # returns a tuple with full import str and the filepath
re_imports = re.compile(r"@import url\(\".*.css\"\);")

def exe_dir():
    """Return the executable directory."""
    if getattr(sys, 'frozen', False):
        exe_path = os.path.dirname(sys.executable)
        exe_path = os.path.dirname(os.path.dirname(os.path.dirname(exe_path))) # Uncomment for macOS app builds
    elif __file__:
        exe_path = os.path.dirname(__file__)
    return exe_path

def read_file(filepath):
    """Return a string with file contents."""
    with open(filepath, mode='rt', encoding='utf-8') as f:
        return f.read()

def resolve_imports(output_str):
    while len(re_imports.findall(output_str)) != 0:
        for imp in re_imports.findall(output_str):
            imp_filepath = "".join(re_imports_filepath.findall(imp))
            imp_filepath_abs = os.path.abspath(imp_filepath)
            try:
                imp_str = read_file(imp_filepath_abs)
                output_str = re.sub(f"@import url\(\"({imp_filepath})\"\);", imp_str, output_str)
                print(f" [+] {imp_filepath_abs}")
            except FileNotFoundError:
                output_str = re.sub(f"@import url\(\"({imp_filepath})\"\);", "/* !importaint; removed broken import */", output_str)
                print(f" [!] {imp_filepath_abs} [file not found]")
        if len(re_imports.findall(output_str)) != 0:
            continue
        else:
            break
    return output_str

def save_str_as_file(str, filepath):
    """Save a string to a file and return the file path."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str)
    return filepath

def main():
    par = argparse.ArgumentParser(description="Merge a CSS file with imports into a single file.")
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    par.add_argument("input_filepath", type=str, help="A CSS file with imports.")
    args = par.parse_args()

    os.chdir(exe_dir())
    output_str = read_file(args.input_filepath)
    output_filepath = os.path.abspath(args.input_filepath.replace(".css", "_compiled.css"))

    print("Resolving the following imports:")
    output_str = resolve_imports(output_str)

    print(f"Saving to: {output_filepath}")
    save_str_as_file(output_str, output_filepath)
    
__main__ = os.path.basename(os.path.abspath(sys.argv[0])).replace(".py","")
if __name__ == "__main__":
    main()