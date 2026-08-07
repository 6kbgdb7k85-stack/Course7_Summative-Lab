import argparse

from utils.utils import fetch_data, fetch_table, parse_int, add_data
from models.user import User
from models.task import Task
from models.project import Project

def get_table(args):
    print(fetch_table(table=args.table))

def get_entry(args):
    print(fetch_data(table=args.table, lookup_key=args.key, lookup_value=parse_int(args.value)))

def main():
    parser = argparse.ArgumentParser(description = "Project Manager CLI")
    subparser = parser.add_subparsers()

    get_table_parser = subparser.add_parser("table", help="Get Table")
    get_table_parser.add_argument("table",help="Name of table")
    get_table_parser.set_defaults(func=get_table)

    get_entry_parser = subparser.add_parser("entry", help="Get Entry from Table")
    get_entry_parser.add_argument("table",help="Name of table")
    get_entry_parser.add_argument("value",help="Value to search for")
    get_entry_parser.add_argument("key",help="Column to search in. Defaults to 'id'", default="id", nargs="?")
    get_entry_parser.set_defaults(func=get_entry)

    args = parser.parse_args()

    if hasattr(args,"func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
