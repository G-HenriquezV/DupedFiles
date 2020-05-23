"""
Main library
"""
from collections import defaultdict
from hashlib import md5
from pathlib import Path


class FileBank:
    """
    Pass
    """

    def __init__(self, folder: str):
        self.path = Path(folder)
        self.files = defaultdict(list)

    def scan_folders(self):
        """
        Appends every file in the folder and subfolders to the self.file list attribute
        """
        for obj in self.path.glob('**/*'):  # https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
            if obj.is_file():
                obj = FileToCheck(obj)
                self.files[obj.hash].append(obj)

    def print_duplicates(self) -> None:
        """
        Prints duplicate items
        """
        for key, value in self.files.items():
            if len(value) > 1:
                print(f'Duplicates found with md5 checksum {key}')
                print(value)


class FileToCheck:
    """
    Object that can be compared
    """

    def __init__(self, file: Path):
        """
        Initializes a FileToCheck object

        :param file: pathlib.Path object pointing to the file
        :type file: Path
        """
        self.file = file
        self.size = file.stat().st_size
        self._md5 = None

    def __eq__(self, other: 'FileToCheck') -> bool:
        """
        Compares to another file to check if it is duplicate. Equivalent to compare_to method

        :param other: FileToCheck type object to compare md5 checksum
        :return: True if the checksum of the other object is the same. False otherwise.
        """
        return self.compare_to(other)

    @property
    def name(self) -> str:
        """
        Returns file name
        """
        return self.file.name

    def _calculate_md5(self) -> str:
        """
        Calculates the md5 checksum of the file, sets the self._md5 attribute and returns it.

        :return: md5 checksum string of the file
        """
        hash_md5 = md5()
        with open(self.file.as_posix(), 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        self._md5 = hash_md5.hexdigest()
        return self._md5

    @property  # Maybe this should not be a property?
    def hash(self) -> str:
        """
        Calculates the md5 checksum of the file if it

        :rtype: str
        :return: md5 checksum of the file
        """
        if self._md5 is None:
            return self._calculate_md5()
        return self._md5

    def compare_to(self, file: 'FileToCheck') -> bool:
        """
        Compares to another file.

        :param file:
        :return: True if md5 checksums are the same. False otherwise.
        """
        if self.size != file.size:
            return False
        else:
            return self.hash == file.hash
