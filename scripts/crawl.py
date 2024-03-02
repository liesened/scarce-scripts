import argparse

from waifuc.action import FilterSimilarAction, \
    ModeConvertAction, FirstNSelectAction, \
    FileExtAction, AlignMaxAreaAction, \
    MinAreaFilterAction
from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource


def crawl(tags: list[str], save_path, limit, key, username, align_images):
    source = DanbooruSource(
        tags, api_key=key, username=username, min_size=None)

    images = source

    if align_images:
        images = images.attach(
            MinAreaFilterAction(1024),
            AlignMaxAreaAction(1024),
        )

    images = images.attach(
        ModeConvertAction('RGB', 'white'),
        FilterSimilarAction('all'),  # filter duplicated images
        FirstNSelectAction(limit),
        # RandomFilenameAction(ext='.png'),  # random rename files
        FileExtAction(ext='.png'),
    )

    images.export(
        # save to directory
        TextualInversionExporter(save_path, use_spaces=True)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Grab pics from danbooru.')
    parser.add_argument('-s', '--search', nargs='+', default=[],
                        help="Search on danbooru. Use underscores. See https://danbooru.donmai.us/wiki_pages/help:cheatsheet")
    parser.add_argument(
        '-o', '--output-dir', help='Path to save the pictures to.', nargs='?', default="")
    parser.add_argument(
        '--limit', help='Select only this much images.', nargs='?', default=400, type=int)
    parser.add_argument(
        '--align-images', action='store_true',
        help="Resize the images to have an area of 1024x1024 and filter them out if they aren't in highres.",)
    parser.add_argument(
        '--username', help='Danbooru username.', nargs='?', default=None)
    parser.add_argument(
        '--api-key', help='Danbooru API key.', nargs='?', default=None)
    args = parser.parse_args()

    if not args.output_dir:
        args.output_dir = args.search[0]

    args.output_dir = args.output_dir.replace(':', '')

    crawl(args.search, args.output_dir, args.limit,
          args.api_key, args.username, args.align_images)
