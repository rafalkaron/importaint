# coding utf-8
__author__ = "Rafał Karoń <rafalkaron@gmail.com>"

import regex as re # needed for Windows builds
import css_html_js_minify
import sys
import os
from .files import (read_external_file,
                    read_file)

#re_css_imports = re.compile(r"(@import url\((\"|\')(.*.css)(\"|\')\);)")
re_css_imports = re.compile(r"(@import.*(\"|\')(.*.css)(\"|\').*;)")
re_external_imports = re.compile(r"(https://|http://|ftp://)")
re_all_imports = re.compile(r"(@import url\((\"|\').*(\"|\')\);)")
re_font_imports_placeholder = re.compile(r"/\* imports placeholder \*/")
re_comments = re.compile(r"/\*[^*]*.*?\*/", flags=re.DOTALL)

def remove_commented_out_imports(output_str):
    """Remove /* commented-out */ imports from a CSS string."""
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
        print(" [!] No imports to resolve.")
        sys.exit(0)
    else:
        print(" [i] Resolving the following imports:")
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
    output_str = css_html_js_minify.css_minify(output_str)
    return output_str