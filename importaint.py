# coding utf-8
"""
Resolve imports in a CSS file.
"""

import sys
import os
import re
import argparse
import requests
import pyperclip

__author__ = "Rafał Karoń <rafalkaron@gmail.com>"
__version__ = "0.9.3"

re_css_imports = re.compile(r"(@import url\((\"|\')(.*.css)(\"|\')\);)")
re_external_imports = re.compile(r"(https://|http://)")
re_all_imports = re.compile(r"(@import url\((\"|\').*(\"|\')\);)")
re_font_imports_placeholder = re.compile(r"/\* imports placeholder \*/")
re_comments = re.compile(r"/\*[^*]*.*?\*/", flags=re.DOTALL)

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

def read_external_file(url):
    """Return a string with external file contents."""
    res = requests.get(url)
    return res.text

def remove_commented_out_imports(output_str):
    comments = re_comments.findall(output_str)
    for comment in comments:
        commented_out_imports = re_all_imports.findall(comment)
        for commented_out_import in commented_out_imports:
            print(" [-] " + commented_out_import[0] + " [removed a commented-out import]")
            comment_new = comment.replace(commented_out_import[0], "!importaint: removed a commented-out import")
            output_str = output_str.replace(comment, comment_new)
    return output_str

def resolve_css_imports(output_str):
    """Replace the @import rules with the target CSS code."""
    if len(re_css_imports.findall(output_str)) == 0:
        print("No imports to resolve.")
        sys.exit(0)
    else:
        print("Resolving the following imports:")
        while True:
            output_str = remove_commented_out_imports(output_str) #output_str = re.sub(re_comments, "", output_str)
            imports = re_css_imports.findall(output_str)
            for imp in imports:
                try:
                    import_full = imp[0]
                    import_filepath = imp[2]
                    import_filepath_abs = os.path.abspath(import_filepath)            
                    if re_external_imports.match(import_filepath):
                        import_str = read_external_file(import_filepath)
                    elif not re_external_imports.match(import_filepath):
                        import_str = read_file(import_filepath_abs)
                    output_str = output_str.replace(import_full, import_str)
                    print(f" [+] {import_filepath}")
                    indirect_imports = re_css_imports.findall(import_str)
                    for indirect_imp in indirect_imports:
                        indirect_import_filepath = indirect_imp[2]
                        indirect_import_filepath_abs = os.path.abspath(indirect_import_filepath)
                        if not os.path.isfile(indirect_import_filepath_abs):
                            if re_external_imports.match(indirect_import_filepath):
                                import_str = read_external_file(indirect_import_filepath)
                            elif not re_external_imports.match(import_filepath):
                                output_str = re.sub(indirect_import_filepath, f"{os.path.dirname(import_filepath_abs)}/{indirect_import_filepath}", output_str)
                except FileNotFoundError:
                    output_str = output_str.replace(import_full, "")
                    print(f" [!] {import_filepath} [file not found]")
            if len(imports) == 0:
                break
            else:
                continue
    return output_str

def move_font_imports(string):
    """Move the @import rules with fonts to the beginning of the code. Remove duplicated strings."""
    output_str = r"/* imports placeholder */" + string
    font_imports = re_all_imports.findall(output_str)
    font_imports = [i[0] for i in font_imports]
    font_imports_no_duplicates = list(dict.fromkeys(font_imports))
    font_imports_str = "\n".join(font_imports_no_duplicates)
    output_str = re.sub(re_all_imports, "", output_str)
    output_str = re.sub(re_font_imports_placeholder, font_imports_str, output_str)
    return output_str

def save_str_as_file(string, filepath):
    """Save a string to a file and return the file path."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(string)
    return filepath

def remove_empty_newlines(output_str):
    """Remove empty newlines from a string."""
    while True:
        output_str = output_str.replace("\n\n", "\n")
        if len(re.findall("\n\n", output_str)) == 0:
            break
        else:
            continue
    return output_str

def remove_redundant_spaces(output_str, redundant_spaces_number, target_spaces_number):
    """Replaces a given number of redundant spaces with a given number of desired spaces."""
    redundant_spaces = " " * redundant_spaces_number
    target_spaces = " " * target_spaces_number
    redundant_spaces = re.findall(redundant_spaces, output_str)
    for redundant_space in redundant_spaces:
        output_str = re.sub(redundant_space, target_spaces, output_str)
    return output_str

def minify_code(output_str):
    """Renders multi-line code into single-line code. Removes spaces. Retains semantic spaces (at least some of them)."""
    output_str = re.sub(r"\n", "", output_str)
    output_str = re.sub(r" ", "", output_str)
    output_str = re.sub("@importurl", "@import url", output_str)
    return output_str

def main():
    par = argparse.ArgumentParser(description="Resolve imports in a CSS file")
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    par.add_argument("-m", "--minify", action="store_true", help="minify the resolved CSS output")
    par.add_argument("-rc", "--remove_comments", action="store_true", help="remove comments from the resolved CSS output")
    par.add_argument("-c", "--copy", action="store_true",help="copy the resolved CSS output to clipboard")
    par.add_argument("input_filepath", type=str, help="provide a filepath to a CSS file with unresolved imports")
    args = par.parse_args()

    os.chdir(os.path.dirname(args.input_filepath))
    output_str = read_file(args.input_filepath)
    output_str = resolve_css_imports(output_str)
    output_str = move_font_imports(output_str)
    output_filepath = os.path.abspath(args.input_filepath.replace(".css", "_compiled.css"))

    if args.minify:
        output_str = minify_code(output_str)
        output_str = re.sub(re_comments, "", output_str)
        print(f"Saved the minified and resolved CSS to: {output_filepath}")
    elif not args.minify:
        output_str = output_str
        output_str = remove_empty_newlines(output_str)
        output_str = remove_redundant_spaces(output_str, 3, 2)
        if args.remove_comments:
            output_str = re.sub(re_comments, "", output_str)
            print(f"Saved the resolved CSS without comments to: {output_filepath}")
        elif not args.remove_comments:
            print(f"Saved the resolved CSS to: {output_filepath}")
    
    save_str_as_file(output_str, output_filepath)
    if args.copy:
        pyperclip.copy(output_str)
        print("Copied the CSS to clipboard.")
    
__main__ = os.path.basename(os.path.abspath(sys.argv[0])).replace(".py","")
if __name__ == "__main__":
    main()