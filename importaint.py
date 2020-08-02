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
__version__ = "0.4"

re_imports = re.compile(r"@import url\(\"(.*.css)\"\);")

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

def get_imports(filepath):
    input_str = read_file(filepath)
    imports = re_imports.findall(input_str)
    imports_absolute = []
    for imp in imports:
        imp_absolute = os.path.abspath(imp)
        imports_absolute.append(imp_absolute)
    return imports_absolute

def get_imports_str(str):
    input_str = str
    imports = re_imports.findall(input_str)
    imports_absolute = []
    for imp in imports:
        imp_absolute = os.path.abspath(imp)
        imports_absolute.append(imp_absolute)
    return imports_absolute

def merge_imports(imports):
    imports_str = []
    for imp in imports:
        try:
            imp_str = read_file(imp)
            print(f" [+] {imp}")
            imports_str.append(f"\n/*!IMPORTAINT; {imp} code*/\n" + imp_str)
        except FileNotFoundError:
            print(f" [!] {imp} [file not found]")
    output_str = "\n\n".join(imports_str)
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

    output_filepath = args.input_filepath.replace(".css", "_compiled.css")
    print(f"Merging the following imports:")
    output_str = merge_imports(get_imports(args.input_filepath))
    
    outstanding_imports = re_imports.findall(output_str) # checks if there are some outstanding, indirect imports
    while len(outstanding_imports) != 0:
        outstanding_str = merge_imports(get_imports_str(output_str)) # resolves the outstanding imports
        output_str = re_imports.sub(outstanding_str, output_str)
        if len(re_imports.findall(output_str)) != 0:
            continue
        else:
            break

    input_file_code_str = re.sub(r"@import url\(\"(.*.css)\"\);", "", read_file(args.input_filepath))
    output_str = output_str + f"\n/*!IMPORTAINT; {args.input_filepath} code*/\n" + input_file_code_str
    print(f"Saving to: {os.path.abspath(output_filepath)}")
    save_str_as_file(output_str, output_filepath)
    
__main__ = os.path.basename(os.path.abspath(sys.argv[0])).replace(".py","")
if __name__ == "__main__":
    main()