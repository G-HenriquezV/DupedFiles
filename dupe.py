"""
Main library
"""
import json
from collections import defaultdict
from hashlib import md5
from pathlib import Path


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

    @property
    def location(self) -> str:
        """
        Returns the full location of the file as a string

        :rtype: str
        :return: Full string of the file location
        """
        return str(self.file.absolute())

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

    def hash(self) -> str:
        """
        Calculates the md5 checksum of the file if it wasn't before. Then returns it.

        :return: md5 checksum of the file
        :rtype: str
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
            return self.hash() == file.hash()


class FileBank:
    """
    TODO: Seriously I have to document everything here
    """

    def __init__(self, folder: str, autorun: bool = True):
        """


        :param folder: Folder to scan
        :param autorun: If checksums and duplicates should be obtained when initialized
        """
        self.path = Path(folder)
        self.files = defaultdict(list)
        self.n_files = 0  # Number of files
        self.duplicates = None
        if autorun:
            self.scan_folders()
            self.get_duplicates()

    def scan_folders(self):
        """
        Appends every file in the folder and subfolders to the self.file list attribute.
        Automatically calculates the md5 checksum of every file
        """
        for obj in self.path.glob('**/*'):  # https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
            if obj.is_file():
                obj = FileToCheck(obj)
                self.files[obj.hash()].append(obj)
                self.n_files += 1

    def get_duplicates(self) -> dict:
        """
        :return: Dictionary with duplicated files
        """
        dupe_dict = {}
        for checksum, files in self.files.items():
            if len(files) > 1:
                dupe_dict[checksum] = files
        self.duplicates = dupe_dict
        return dupe_dict

    def print_duplicates(self) -> None:
        """
        Prints duplicate items
        """
        for key, value in self.duplicates.items():
            file_locations = map(lambda p: p.location, value)
            print(f'MD5: {key}')
            print('Files:')
            for file in file_locations:
                print(f'- {file}')

    def save_json(self) -> None:
        """
        Saves a json file, named duplicates.json, at the cwd with every duplicated file.
        """
        with open('duplicates.json', 'w', encoding='utf-8') as f:
            json.dump(self.duplicates, f, indent=2, ensure_ascii=False)
