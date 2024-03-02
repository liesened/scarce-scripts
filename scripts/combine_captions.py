#!/usr/bin/python

import argparse

from fnmatch import fnmatch
from pathlib import Path


def combine_files(input_dir1, input_dir2, output_dir, meta_file=None, threshold=-1):
    input_dir1 = Path(input_dir1)
    input_dir2 = Path(input_dir2)
    output_dir = Path(output_dir)

    meta_tags = []
    if meta_file is not None:
        with open(meta_file, 'r') as f:
            meta_tags = [x.strip() for x in f.readlines()]

    if not output_dir.is_dir():
        output_dir.mkdir(parents=True)

    for file1 in input_dir1.glob('*.txt'):
        file2 = input_dir2 / file1.name

        if not file2.exists():
            continue

        output_file = output_dir / file1.name

        with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out_file:
            tags1 = [x.strip() for x in f1.read().split(',')]
            tags2 = [x.strip() for x in f2.read().split(',')]

            tags_combined = combine_tags(
                tags1, tags2, meta_tags, threshold)

            out_file.write(', '.join(tags_combined))


def combine_tags(tags1, tags2, meta_tags, threshold):
    tags_combined = set()

    for tag in tags1:

        to_add = True

        for meta_tag in meta_tags:
            if fnmatch(tag, meta_tag):
                to_add = False

        if to_add:
            tags_combined.add(tag)

    for tag in tags2:
        if len(tags_combined) > threshold:
            break
        
        if tag in tags_combined:
            continue

        to_add = True

        for meta_tag in meta_tags:
            if fnmatch(tag, meta_tag):
                to_add = False

        if to_add:
            tags_combined.add(tag)

    return tags_combined


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Combine files with comma-separated tags')
    parser.add_argument('-t', '--tag-threshold', type=int, nargs='?', default=-1,
                        help="Don't add tags from dir2 if there's this much tags in dir1.")
    parser.add_argument(
        '-m', '--meta_file', help='Path to the file with tags to be removed', nargs='?')
    parser.add_argument('input_dir1', help='Path to the first input directory')
    parser.add_argument(
        'input_dir2', help='Path to the second input directory (autotagged)')
    parser.add_argument('output_dir', help='Path to the output directory')
    args = parser.parse_args()

    combine_files(args.input_dir1, args.input_dir2,
                  args.output_dir, args.meta_file, args.tag_threshold)
