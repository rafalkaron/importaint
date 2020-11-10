# importaint
Merge a CSS file with imports into a single file.

## Before you begin
* Download the latest **importaint** version. See [Download](https://github.com/rafalkaron/importaint/releases/latest).
* Unzip **importaint**.

## Usage
1. Run **important** followed by the local path or ULR to the CSS file that you want to compile.

## Optional Attributes
You can pass the following arguments to control the **importaint** behavior.
* `--minify` - minify the resolved CSS output (experimental!)
* `--remove_comments` - remove comments from the resolved CSS output
* `--copy` - copy the resolved CSS output to system clipboard

## Example - Local File (Without Comments)
```shell
importaint "C:\GitHub\styling\style.css" --remove_comments
```

## Result
* In the original CSS file directory, a new resolved CSS file without `/* comments */` is created.  
 `C:\GitHub\styling\style_compiled.css`

## Example - Remote File (Minified and Copied)
```shell
importaint "https://mysite.com/styles/style.css" --minify
```

## Result
* In the selected directory:
    * The remote unresolved CSS file is created
    * A new resolved and minified CSS file is created