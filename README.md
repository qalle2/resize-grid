# resize-grid
A command line tool that reads a grid-based image and writes another image with a larger grid. Each &ldquo;tile&rdquo; (rectangle) in the grid will be padded with the specified background color to the new size and centered (not resized).

Requires Python and the [Pillow module](https://python-pillow.org).

## Command line arguments
*options* *inputFile* *outputFile*
* *options* are any number of these, separated by spaces:
  * `--itw N`: Width of each tile in input file, in pixels. `N` is 2 to 256. The default is 8.
  * `--ith N`: Height of each tile in input file, in pixels. `N` is 2 to 256. The default is 8.
  * `--otw N`: Width of each tile in output file, in pixels. `N` is 2 to 256. The default is 9.
  * `--oth N`: Height of each tile in output file, in pixels. `N` is 2 to 256. The default is 9.
  * `--bgcolor C`: Background color in output file. Hexadecimal RRGGBB code, `000000`&ndash;`ffffff`. The default is `000000` (black).
* *inputFile*: Image file to read (e.g. PNG).
  * Required.
  * The width must be a multiple of input tile width.
  * The height must be a multiple of input tile height.
  * No alpha channel.
* *outputFile*: PNG file to write.
  * Required.
  * The width will be (input image width) / (input tile width) &times; (output tile width).
  * The height will be (input image height) / (input tile height) &times; (output tile height).

## Example
`python3 resizegrid.py sample-before.png sample-after.png --itw 8 --ith 8 --otw 10 --oth 12 --bgcolor 0000ff`

Before and after:

![before](sample-before.png)
![after](sample-after.png)

(The images were actually 16&times;16 and 20&times;24 pixels; they've been resized to 5x their original size afterwards.)
