from waifuc.action import FilterSimilarAction, ModeConvertAction, RandomFilenameAction
from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource


def crawl(tags: list[str]):

    s = DanbooruSource(tags)

    # crawl images, process them, and then save them to directory with given format
    s.attach(
        ModeConvertAction('RGB', 'white'),
        FilterSimilarAction('all'),  # filter duplicated images
        RandomFilenameAction(ext='.png'),  # random rename files
    ).export(
        # save to surtr_dataset directory
        TextualInversionExporter(tags[0].replace(':', ''), use_spaces=True)
    )


if __name__ == '__main__':
    crawl(['sparkle_(honkai:_star_rail)'])
