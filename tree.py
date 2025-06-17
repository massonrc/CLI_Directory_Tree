"""
This module will provide the RP Tree main module
"""
import os
import pathlib

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
