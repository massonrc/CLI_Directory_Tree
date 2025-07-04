"""
This module will provide the RP Tree main module
"""
import os
import pathlib
import sys
from collections import deque

# Define connector characters for tree diagram
PIPE = "|"
ELBOW = "'--"
TEE = "|--"
PIPE_PREFIX = "|   "
SPACE_PREFIX = "    "

class DirectoryTree:
    def __init__(self, root_dir, dir_only = False, output_file = sys.stdout):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        tree = deque(self._generator.build_tree()) # holds result of calling build_tree

        if self._output_file != sys.stdout:
            # Wrap the tree in a markdown code block
            tree.appendleft( "```")
            tree.append("```")
            self._output_file = open(
                self._output_file, mode = "w", encoding = "utf-8"
            )

        with self._output_file as stream:
            # Loop through to print each tree entry
            for entry in tree:
                print(entry, file = stream)


class _TreeGenerator:
    def __init__(self, root_dir, dir_only = False):
        """
        Constructor
        :param root_dir:
        """
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = [] # Shape the directory tree diagram


    def build_tree(self):
        """
        This will return the directory tree diagram.
        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """
        This will add the name of the root directory to ._tree
        """
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        """
        This will add the name of the directory to the _tree
        :param directory: Holds the path to the directory you want to walk through. A Path object.
        :param prefix: Holds a prefix string that you use to draw the tree diagram on the terminal window
        :return: None
        """
        entries = self._prepare_entries(directory) # prepare directory entries to generate either full or directory only
        entries_count = len(entries) # get number of entries in directory

        # Loop over entries in directory, use enumerate to associate an index to each entry
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries

        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        """
        Helper method
        Returns: None
        """

        self._tree.append(f"{prefix}{connector}{directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX

        else:
            prefix += SPACE_PREFIX

        # Tree_body calls itself by means of ._add_directory() until it traverses the whole directory structure
        self._tree_body(
            directory = directory,
            prefix = prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        """
        This method will append a file entry to the directory tree list

        Returns: None
        """
        self._tree.append(f"{prefix}{connector}{file.name}")