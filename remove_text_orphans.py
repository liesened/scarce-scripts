#!/usr/bin/python

import argparse
import pathlib

img_suffixes = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
    ".jxl"
]


def main(args):

    directory = pathlib.Path(args.directory)

    for file in directory.glob('*.txt'):

        to_be_removed = True

        for suffix in img_suffixes:
            image_file = file.with_suffix(suffix)

            if image_file.exists():
                to_be_removed = False

        if to_be_removed:
            file.unlink()

            print(
                f"Deleted text file '{file.name}' because corresponding image file does not exist.")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Remove text files without corresponding images.")

    parser.add_argument(
        "directory", help="The directory to scan for text files and corresponding images.")

    args = parser.parse_args()

    main(args)
