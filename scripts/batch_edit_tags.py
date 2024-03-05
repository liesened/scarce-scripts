import argparse
import sys
import unittest

from pathlib import Path
from dataclasses import dataclass


def run_processor(args):
    directory = Path(args.directory)

    tag_processor = args.processor

    for caption_path in directory.glob('*.txt'):
        with open(caption_path, "rw") as f:
            caption = f.readline()
            new_caption = tag_processor(args, caption)
            f.seek(0)
            f.write(new_caption)
            f.truncate()


def run_tests(args):
    unittest.main(verbosity=2)


def caption_to_tags(caption: str, delimeter = ',') -> list[str]:
    return [tag.strip() for tag in caption.split(delimeter)]

def tags_to_caption(tags: list[str], delimeter = ',', use_underscore = False):
    if use_underscore:
        tags = [tag.replace(' ', '_') for tag in tags]
    
    return (delimeter + ' ').join(tags)


def add_processor(args, caption: str) -> str:
    tags = caption_to_tags(caption)
    
    to_add = args.tags
    
    if isinstance(to_add, str):
        to_add = [to_add]
    
    if args.prepend:
        for tag in to_add[::-1]:
            tags.insert(0, tag)
    
    if args.append:
        for tag in to_add:
            tags.append(tag)
    
    if args.after:
        pos = tags.index(args.after)
        if pos != -1:
            for tag in to_add[::-1]:
                tags.insert(pos+1, tag)
                
    if args.before:
        pos = tags.index(args.before)
        if pos != -1:
            for tag in to_add[::-1]:
                tags.insert(pos, tag)
    
            
    return tags_to_caption(tags)


def delete_processor(args, caption: str) -> str:
    print("Not implemented.")
    print(args, caption)


def edit_processor(args, caption: str) -> str:
    print("Not implemented.")
    print(args, caption)


class TestBatchEditing(unittest.TestCase):

    def test_add(self):
        args = dataclass()
        
        caption = "a, b, c, d, e, f"
        args.tags = ["123", '789']
        args.prepend = True
        args.append = True
        args.before = 'e'
        args.after = 'd'
        expected_caption =  "123, 789, a, b, c, d, 123, 789, 123, 789, e, f, 123, 789"
        result_caption = add_processor(args, caption)
        
        self.assertEqual(result_caption, expected_caption)
        
        # No prepend
        args.prepend = False
        expected_caption = "a, b, c, d, 123, 789, 123, 789, e, f, 123, 789"
        result_caption = add_processor(args, caption)
        
        self.assertEqual(result_caption, expected_caption)
        
        # No append
        args.append = False
        expected_caption = "a, b, c, d, 123, 789, 123, 789, e, f"
        result_caption = add_processor(args, caption)
        
        self.assertEqual(result_caption, expected_caption)
        
        # No after
        args.append = False
        expected_caption = "a, b, c, d, 123, 789, 123, 789, e, f"
        result_caption = add_processor(args, caption)
        
        self.assertEqual(result_caption, expected_caption)
        
test = TestBatchEditing


def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    subparsers = parser.add_subparsers(title='actions',
                                       help='Batch add, edit, or delete tags', required=True)

    def add_directory(parser):
        parser.add_argument('-d', '--directory', type=str, required=True,
                            help='The dataset directory to work on')

    # Add
    parser_add = subparsers.add_parser(
        'add', help='Insert a tag to every caption')

    parser_add.add_argument('--prepend', action='store_true',
                            help="Insert a new tag at the start of the caption")
    parser_add.add_argument('--append', action='store_true',
                            help="Insert a new tag at the end of the caption")
    parser_add.add_argument('--after', type=str,
                            help="Insert a new tag after this tag")
    parser_add.add_argument('--before', type=str,
                            help="Insert a new tag before this tag")

    parser_add.add_argument('tags', default=[], nargs='+')

    parser_add.set_defaults(processor=add_processor)
    add_directory(parser_add)

    # Delete
    parser_delete = subparsers.add_parser(
        'del',
        help='Remove a tag from every caption if it exists')

    parser_delete.add_argument('tags', default=[], nargs='+')

    parser_delete.set_defaults(processor=delete_processor)
    add_directory(parser_delete)

    # Edit
    parser_edit = subparsers.add_parser(
        'edit', help='Change a tag or a string to something else')

    edit_group = parser_edit.add_mutually_exclusive_group()
    edit_group.add_argument(
        '--str', action='store_true', help="Search for a specific string to replace instead of tags")
    edit_group.add_argument(
        '--re', action='store_true', help="Use regex to find and replace a string")

    parser_edit.add_argument('--old', nargs='+')
    parser_edit.add_argument('--new', nargs='+')

    parser_edit.set_defaults(processor=edit_processor)
    add_directory(parser_edit)

    # Tests
    subparsers.add_parser("test", help="Run tests").set_defaults(
        runner=run_tests)
    parser.set_defaults(runner=run_processor)

    args = parser.parse_args()

    args.runner(args)


if __name__ == '__main__':
    main()
