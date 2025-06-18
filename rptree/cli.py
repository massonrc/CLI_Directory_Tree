"""
This module will provide the RP Tree CLI.
"""
import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree

def main():
    args = parse_cmd_line_arguments() # pack command line arguments in args
    root_dir = pathlib.Path(args.root_dir)

    if not root_dir.is_dir():
        print("The specified root directory does not exist.")
        sys.exit()

    tree = DirectoryTree(root_dir, dir_only = args.dir_only, output_file = args.output_file)
    tree.generate()

def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog = "tree",
        description="RP Tree, a directory tree generator",
        epilog="Thanks for using RP Tree!"
    )

    parser.version = f"RP Tree v{__version__}"
    parser.add_argument("-v", "--version", action="version") # Add first optional argument to CLI
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR", # Hold name of argument in usage messages
        nargs="?", # Defines number of values program can take at hand. ? denotes only one directory path at CL
        default=".", # Default value for argument at hand, set to the current directory as def root directory
        help="Generate a full directory tree starting at ROOT_DIR" # Msg for what the argument does
    )

    # Add -d and --dir-only flags to CLI
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree"
    )

    # Add -o and --outputfile-file flags
    parser.add_argument(
        "o",
        "--output-file",
        metavar = "OUTPUT_FILE",
        nargs = "?",
        default = sys.stdout,
        help = " Generate a full directory tree and save it to a file"
    )

    return parser.parse_args()