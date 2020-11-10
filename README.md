# importaint
Compile a CSS file with imports into a resolved CSS file without imports.

## Before you begin
* Download the latest **importaint** version. See [Download](https://github.com/rafalkaron/importaint/releases/latest).
* Unzip **importaint**.

## Usage
1. In a terminal app, run **important** followed by the local path or URL to the CSS file that you want to compile.  
    **NOTE:** You can pass the following optional arguments to control the **importaint** behavior.
      * `--minify` or `-m` - minify the resolved CSS
      * `--remove_comments` or `-rc` - remove `/* comments */` from the resolved CSS
      * `--copy` or `-c` - copy the resolved CSS output to system clipboard
2. If needed, accept any security prompt. For more information, see [Accepting macOS Security Prompts](https://github.com/rafalkaron/importaint/wiki/Accepting-macOS-Security-Prompts) or [Accepting Windows Security Prompts](https://github.com/rafalkaron/importaint/wiki/Accepting-Windows-Security-Prompts)

## Example - Local File (Removed Comments)
```shell
importaint "C:\GitHub\styling\style.css" --remove_comments
```

### Result
In the original CSS file directory, a new resolved CSS file without `/* comments */` is created: `C:\GitHub\styling\style_compiled.css`

## Example - Remote File (Minified and Copied)
```shell
importaint "https://mysite.com/styles/style.css" --minify --copy
```

### Result
In the local directory that you are prompted about:
  * The remote unresolved CSS file is downloaded
  * A new resolved and minified CSS file is created