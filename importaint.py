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
__version__ = "0.9"

re_imports = re.compile(r"(@import url\((\"|\')(.*.css)(\"|\')\);)") # returns a tuple with full import str and the filepath #add or operand for ' ' imports
re_comments = re.compile(r"/\*[^*]*.*?\*/", flags=re.DOTALL)
re_font_imports = re.compile(r"(@import url\((\"|\').*(\"|\')\);)")

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
    print("Resolving the following imports:")
    while True:
        imports = re_imports.findall(output_str)
        output_str = re.sub(re_comments, "", output_str)
        for imp in imports:
            try:
                import_full = imp[0]
                import_filepath = imp[2]
                import_filepath_abs = os.path.abspath(import_filepath)            
                import_str = read_file(import_filepath_abs)
                output_str = output_str.replace(import_full, import_str)
                print(f" [+] {import_filepath_abs}")
                indirect_imports = re_imports.findall(import_str)
                for indirect_imp in indirect_imports:
                    indirect_import_filepath = indirect_imp[2]
                    indirect_import_filepath_abs = os.path.abspath(indirect_import_filepath)
                    if not os.path.isfile(indirect_import_filepath_abs):
                        output_str = re.sub(indirect_import_filepath, f"{os.path.dirname(import_filepath_abs)}/{indirect_import_filepath}", output_str)
                        output_str = re.sub(re_comments, "", output_str)
            except FileNotFoundError:
                output_str = output_str.replace(import_full, "")
                print(f" [!] {import_filepath_abs} [file not found]")
            output_str = re.sub(re_comments, "", output_str)
        if len(imports) == 0:
            break
        else:
            continue
 
    output_str = re.sub(re_comments, "", output_str)
    return output_str

def save_str_as_file(str, filepath):
    """Save a string to a file and return the file path."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str)
    return filepath

def main():
    par = argparse.ArgumentParser(description="Merge a CSS file with imports into a single file.")
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    par.add_argument("-m", "--minify", action="store_true", help="Minify CSS.")
    par.add_argument("input_filepath", type=str, help="A CSS file with imports.")
    args = par.parse_args()

    os.chdir(exe_dir())
    output_str = read_file(args.input_filepath)
    output_filepath = os.path.abspath(args.input_filepath.replace(".css", "_compiled.css"))

    imports_placeholder = "/* imports placeholder */"
    re_imports_placeholder = re.compile(r"/\* imports placeholder \*/")
    output_str = imports_placeholder + resolve_imports(output_str)

    font_imports = re_font_imports.findall(output_str)
    font_imports = [i[0] for i in font_imports]
    font_imports = "\n".join(font_imports)

    output_str = re.sub(re_font_imports, "", output_str)
    output_str = re.sub(re_imports_placeholder, font_imports, output_str)

    if args.minify:
        print(f"Saving minified CSS to: {output_filepath}")
        output_str = output_str.strip().replace("\n", "").replace(" ", "").replace("@importurl", "@import url") # This messes up font improts/added ugly workaround
    elif not args.minify:
        output_str = output_str.strip().replace("\n\n", "\n")
        print(f"Saving CSS to: {output_filepath}")
    
    save_str_as_file(output_str, output_filepath)
    
__main__ = os.path.basename(os.path.abspath(sys.argv[0])).replace(".py","")
if __name__ == "__main__":
    main()