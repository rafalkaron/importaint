# coding utf-8
"""
Compile a CSS file with imports into a resolved CSS file without imports.
"""

import os
import re
import argparse
from importaint import (read_file,
                        read_external_file,
                        save_str_as_file,
                        resolve_css_imports,
                        move_font_imports,
                        remove_empty_newlines,
                        remove_redundant_spaces,
                        minify_code)

__author__ = "Rafał Karoń <rafalkaron@gmail.com>"
__version__ = "0.9.5"

def main():
    par = argparse.ArgumentParser(description="Compile a CSS file with imports into a resolved CSS file without imports.")
    par.add_argument("input_path", type=str, help="a filepath or URL to a CSS file with imports that you want to compile")
    par.add_argument("-out", "--output", metavar="output_dir", help="manually specify the output folder. For remote files, defaults to desktop. For local files, defaults to the input file folder.")
    par.add_argument("-m", "--minify", action="store_true", help="minify the compiled CSS")
    par.add_argument("-rc", "--remove_comments", action="store_true", help="remove comments from the compiled CSS")
    par.add_argument("-c", "--copy", action="store_true",help="copy the compiled CSS to clipboard")
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    args = par.parse_args()

    re_external_imports = re.compile(r"(https://|http://|ftp://)")
    re_comments = re.compile(r"/\*[^*]*.*?\*/", flags=re.DOTALL)

    output_dir = args.output

    if re_external_imports.match(args.input_path):
        remote_file = os.path.basename(args.input_path)
        if not args.output:
            output_dir = input("""Clone the external unresolved CSS by doing any of the following:
   * Enter the local directory in which you want to save the file
   * Save the file to Desktop by pressing [Enter] 
> """).replace("\"","").replace("\'","")
        new_file = f"{output_dir}/{remote_file}"
        if not os.path.isdir(output_dir):
            new_file = f"{os.path.normpath(os.path.expanduser('~/Desktop'))}/{remote_file}"
            print(f" [i] No path or invalid path. Copying the external unresolved CSS file to: {new_file}")
        else:
            print(f" [i] Copying the original remote CSS file to: {new_file}")
        
        if os.path.isfile(new_file):
            prompt = input(f" [?] Do you want to overwrite {new_file}? [y/n]: ")
            if prompt == "y" or prompt == "Y":
                pass
            elif prompt != "y" or prompt != "Y":
                print(f" [i] Cancelled.")
                return False
            
        save_str_as_file(read_external_file(args.input_path), new_file)
        output_str = read_external_file(args.input_path)
        output_filepath = os.path.abspath(new_file.replace(".css", "_compiled.css"))
        os.chdir(os.path.dirname(new_file))
    else:
        output_str = read_file(args.input_path)
        if args.output:
            output_filepath = args.output + os.path.basename(args.input_path.replace(".css", "_compiled.css"))
        if not args.output:
            output_filepath = os.path.abspath(args.input_path.replace(".css", "_compiled.css"))
        os.chdir(os.path.dirname(args.input_path))

    output_str = resolve_css_imports(output_str)
    output_str = move_font_imports(output_str)

    if args.minify:
        output_str = minify_code(output_str)
        print(f" [i] Minified the resolved CSS")

    if args.remove_comments:
        output_str = re.sub(re_comments, "", output_str)
        print(f" [i] Removed comments from the resolved CSS")

    output_str = remove_empty_newlines(output_str)
    output_str = remove_redundant_spaces(output_str, 3, 2)
    
    if args.copy:
        pyperclip.copy(output_str)
        print(" [i] Copied the resolved CSS to clipboard.")
    
    if os.path.isfile(output_filepath):
        prompt = input(f" [?] Do you want to overwrite {output_filepath}? [y/n]: ")
        if prompt == "y" or prompt == "Y":
            pass
        elif prompt != "y" or prompt != "Y":
            print(f" [i] Cancelled.")
            return False

    save_str_as_file(output_str, output_filepath)
    print(f" [✔] Saved the resolved CSS to: {output_filepath}")
    
if __name__ == "__main__":
    main()