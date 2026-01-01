# auto_search_projectfolder.py
import os

def find_file_in_project(filename, start_dir=None):
    """
    Search for a file in the project folder recursively.

    Args:
        filename (str): Name of the file to search for.
        start_dir (str, optional): Directory to start search from.
                                   Defaults to the project root (one level above this file).

    Returns:
        str: Absolute path to the found file.

    Raises:
        FileNotFoundError: If the file is not found anywhere in the project.
    """
    if start_dir is None:
        # Default start_dir is the parent of this script
        start_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)

    raise FileNotFoundError(f"Cannot find '{filename}' in project folder '{start_dir}'")
