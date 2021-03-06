# importaint
Compile a CSS file with imports into a resolved CSS file without imports.

## Before you begin
1. Download the latest **importaint** version. See [Download](https://github.com/rafalkaron/importaint/releases/latest).
1. Unzip **importaint**.

## Usage
1. In a terminal app, run **important** followed by the local path or URL to the CSS file that you want to compile.  
    **NOTE:** You can pass the following optional arguments to control the **importaint** behavior.
      * `--output` or `-out` - define the output directory
      * `--minify` or `-m` - minify the resolved CSS
      * `--remove_comments` or `-rc` - remove `/* comments */` from the resolved CSS
      * `--copy` or `-c` - copy the resolved CSS output to system clipboard
2. If needed, accept any security prompt. For more information, see [Accepting macOS Security Prompts](https://github.com/rafalkaron/importaint/wiki/Accepting-macOS-Security-Prompts) or [Accepting Windows Security Prompts](https://github.com/rafalkaron/importaint/wiki/Accepting-Windows-Security-Prompts).

## Examples

### Local File - compiled without comments
```shell
importaint "C:\GitHub\styling\style.css" --remove_comments
```

#### Result
In the original CSS file directory, a new resolved CSS file without `/* comments */` is created: `C:\GitHub\styling\style_compiled.css`

### Remote File - compiled, minified, and copied to clipboard
```shell
importaint "https://mysite.com/styles/style.css" --minify --copy
```

#### Result
In the local directory that you are prompted about:
  * The remote unresolved CSS file is downloaded
  * A new resolved and minified CSS file is created

### Remote file - compiled and saved to a custom output folder
```shell
importaint "https://mysite.com/styles/style.css" -out "C:\MyStyles\StyleA"
```

#### Result
In the output directory that you provided (`C:\MyStyles\StyleA`)
  * The remote unresolved CSS file is downloaded
  * A new resolved CSS file is created