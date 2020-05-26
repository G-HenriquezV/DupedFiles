"""
Main library
"""
import json
from collections import defaultdict
from hashlib import md5
from pathlib import Path
from typing import Optional, Any, Union


class FileToCheck:
    """
    Object that includes a file. Can be compared to another file.
    """

    def __init__(self, file: Path):
        """
        Initializes a FileToCheck object

        :param file: pathlib.Path object pointing to the file
        :type file: Path
        """
        self.file = file
        self.size = file.stat().st_size
        self._md5 = None  # MD5 Hash string

    def __eq__(self, other: 'FileToCheck') -> bool:
        """
        Compares to another file to check if it is duplicate

        :param other: FileToCheck type object to compare md5 checksum
        :return: True if the checksum of the other object is the same. False otherwise.
        """
        if not isinstance(other, FileToCheck):
            return False
        return self.size == other.size and self.md5 == other.md5

    @property
    def name(self) -> str:
        """
        Returns file name
        """
        return self.file.name

    @property
    def absolute_loc(self) -> str:
        """
        Returns the full location of the file as a string

        :rtype: str
        :return: Full string of the file location
        """
        return str(self.file.absolute())

    def _calculate_md5(self) -> None:
        """
        Calculates the md5 checksum of the file, sets the self._md5 attribute and returns it.

        :return: md5 checksum string of the file
        """
        hash_md5 = md5()
        with open(self.file.as_posix(), 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        self._md5 = hash_md5.hexdigest()

    @property
    def md5(self) -> str:
        """
        Calculates the md5 checksum of the file if it wasn't before. Then returns it.

        :return: md5 checksum of the file
        :rtype: str
        """
        if self._md5 is None:
            self._calculate_md5()
        return self._md5


class FileBank:
    """
    Class to analyze a folder for duplicate files
    """

    def __init__(self, folder: str, autorun: bool = True):
        """
        :param folder: Folder to scan
        :param autorun: If true checksums and duplicates should be obtained when initialized
        """
        if not (path := Path(folder)).is_dir():
            raise NotADirectoryError('Folder does not exist!')
        self.path = path
        self.files = defaultdict(list)
        self.duplicates = None
        if autorun:
            self.scan_folders()
            self.get_duplicates()

    def scan_folders(self) -> None:
        """
        Appends every file in the folder and subfolders to the self.file list attribute.
        Automatically calculates the md5 checksum of every file
        """
        for obj in self.path.glob('**/*'):  # https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
            if obj.is_file():
                obj = FileToCheck(obj)
                self.files[obj.md5].append(obj)

    def get_duplicates(self) -> None:
        """
        :return: Dictionary with duplicated files
        """
        dupe_dict = {}
        for checksum, files in self.files.items():
            if len(files) > 1:
                dupe_dict[checksum] = files
        self.duplicates = dupe_dict

    def print_duplicates(self) -> None:
        """
        Prints duplicate items
        """
        for key, value in self.duplicates.items():
            print('\n')
            print(f'MD5: {key.upper()}')
            for file in value:
                print(f'- {file.absolute_loc}')

    def save_json(self) -> None:
        """
        Saves a json file, named duplicates.json, at the cwd with every duplicated file.
        """
        dump_dict = {}
        for key, file_checks in self.duplicates.items():
            dump_dict[key] = [file_check.absolute_loc for file_check in file_checks]

        with open('duplicates.json', 'w', encoding='utf-8') as f:
            json.dump(dump_dict, f, indent=2, ensure_ascii=False)
