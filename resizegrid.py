# enlarge the grid of a grid-based image

import argparse, os, sys
try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    sys.exit("Pillow module required. See https://python-pillow.org")

def decode_color_code(colorStr):
    # decode a hexadecimal RRGGBB color code into (red, green, blue)
    try:
        color = int(colorStr, 16)
        if not 0 <= color <= 0xffffff:
            raise ValueError
    except ValueError:
        sys.exit("Unrecognized color code: " + colorStr)
    return tuple((color >> s) & 0xff for s in (16, 8, 0))

def parse_arguments():
    # parse command line arguments

    parser = argparse.ArgumentParser(
        description="Enlarge the grid of a grid-based image. See README.md "
        "for more info."
    )

    parser.add_argument("--itw", type=int, default=8)
    parser.add_argument("--ith", type=int, default=8)
    parser.add_argument("--otw", type=int, default=9)
    parser.add_argument("--oth", type=int, default=9)
    parser.add_argument("--bgcolor", type=str, default="000000")

    parser.add_argument("inputfile")
    parser.add_argument("outputfile")

    args = parser.parse_args()

    intArgValues = (args.itw, args.ith, args.otw, args.oth)
    if min(intArgValues) < 2 or max(intArgValues) > 256:
        sys.exit("Tile widths and heights must be 2-256.")

    if args.otw < args.itw:
        sys.exit("Output tiles must be at least as wide as input tiles.")
    if args.oth < args.ith:
        sys.exit("Output tiles must be at least as tall as input tiles.")
    if args.otw == args.itw and args.oth == args.ith:
        sys.exit(
            "Output tiles must be larger than input tiles in at least one "
            "dimension."
        )

    decode_color_code(args.bgcolor)  # just validate for now

    if not os.path.isfile(args.inputfile):
        sys.exit("Input file not found.")
    if os.path.exists(args.outputfile):
        sys.exit("Output file already exists.")

    return args

def convert_image(source, args):
    # source: source image
    # return: target image

    if source.width == 0 or source.width % args.itw:
        sys.exit("Image width is not a multiple of input tile width.")
    if source.height == 0 or source.height % args.ith:
        sys.exit("Image height is not a multiple of input tile height.")

    if source.mode in ("L", "P"):
        source = source.convert("RGB")
    elif source.mode != "RGB":
        sys.exit(
            "Unsupported input pixel format (try removing the alpha channel)."
        )

    # input image width & height in tiles
    tileColumns = source.width  // args.itw
    tileRows    = source.height // args.ith

    # pixel offset in output image (to center the tiles)
    outputXOffset = (args.otw - args.itw) // 2
    outputYOffset = (args.oth - args.ith) // 2

    # create output image
    target = Image.new(
        "RGB", (tileColumns * args.otw, tileRows * args.oth),
        decode_color_code(args.bgcolor)
    )

    # create a temporary image for copying each tile
    tileImage = Image.new(
        "RGB", (args.itw, args.ith), decode_color_code(args.bgcolor)
    )

    for ty in range(tileRows):
        for tx in range(tileColumns):
            # copy tile from input image to temporary image
            x = tx * args.itw
            y = ty * args.ith
            tile = tuple(
                source.crop((x, y, x + args.itw, y + args.ith)).getdata()
            )
            tileImage.putdata(tile)
            # copy temporary image to center of corresponding tile in output
            # image
            x = tx * args.otw + outputXOffset
            y = ty * args.oth + outputYOffset
            target.paste(tileImage, (x, y))

    return target

def main():
    args = parse_arguments()

    try:
        with open(args.inputfile, "rb") as source, \
        open(args.outputfile, "wb") as target:
            source.seek(0)
            sourceImage = Image.open(source)
            targetImage = convert_image(sourceImage, args)
            target.seek(0)
            targetImage.save(target, "png")
    except UnidentifiedImageError:
        sys.exit("Unrecognized input image format.")
    except OSError:
        sys.exit("Error reading/writing files.")

main()
