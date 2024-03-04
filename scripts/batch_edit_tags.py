import argparse
import sys


def add(args):
    print("Not implemented.")
    print(args)


def delete(args):
    print("Not implemented.")
    print(args)


def edit(args):
    print("Not implemented.")
    print(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    subparsers = parser.add_subparsers(title='actions',
                                       help='Batch add, edit, or delete tags', required=True)

    def add_directory(parser):
        parser.add_argument('directory', type=str,
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
    parser_add.set_defaults(func=add)
    add_directory(parser_add)

    # Delete
    parser_delete = subparsers.add_parser(
        'del',
        help='Remove a tag from every caption if it exists')
    parser_delete.add_argument('tags', default=[], nargs='+')
    parser_delete.set_defaults(func=delete)
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

    parser_edit.set_defaults(func=edit)

    add_directory(parser_edit)

    args = parser.parse_args()
    args.func(args)
