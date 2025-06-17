"""
This module will provide the RP Tree main module
"""
import os
import pathlib
from rptree.cli import main

# Define connector characters for tree diagram
PIPE = "|"
ELBOW = "'--"
TEE = "|--"
PIPE_PREFIX = "|   "
SPACE_PREFIX = "    "

class DirectoryTree:
    def __init__(self, root_dir):
        self.generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree() # holds result of calling build_tree

        # Loop through to print each tree entry
        for entry in tree:
            print(entry)


class _TreeGenerator:
    def __init__(self, root_dir):
        """
        Constructor
        :param root_dir:
        """
        self._root_dir = pathlib.Path(root_dir)
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
        entries = directory.iterdir() # Assign result to entries, returns subdirectories in directory
        entries = sorted(entries, key = lambda entry: entry.is_file())
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

if __name__=="__main__":
    main()