"""
This module will provide the RP Tree CLI.
"""
import argparse
import pathlib
import sys

from . import __version__
from rptree.rptree import DirectoryTree

def main():
    args = parse_cmd_line_arguments() # pack command line arguments in args
    root_dir = pathlib.Path(args.root_dir)

    if not root_dir.is_dir():
        print("The specified root directory does not exist.")
        sys.exit()

    tree = DirectoryTree(root_dir)
    tree.generate()