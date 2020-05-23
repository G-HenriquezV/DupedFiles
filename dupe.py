"""
Main library
"""
from hashlib import md5
from itertools import combinations
from pathlib import Path


class FileBank:
    """
    Pass
    """

    def __init__(self, folder: str):
        self.path = Path(folder)
        self.files = []

    def scan_folders(self):
        """
        Appends every file in the folder and subfolders to the self.file list attribute
        """
        for obj in self.path.glob('**/*'):  # https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
            if obj.is_file():
                self.files.append(File(obj))

    def run_comparisons(self):
        """
        Compares every file in self.files list
        # TODO: Create a list or dictionary that lists every matching file
        """
        for f1, f2 in combinations(self.files, 2):
            if f1.compare_to(f2) is True:
                print(f'{f1.name} matches with {f2.name}')
            else:
                # print(f'{f1.name} does not match {f2.name}')
                pass


class File:
    """
    TODO
    """

    def __init__(self, file: Path):
        """
        Initializes a File object

        :param file: pathlib.Path object pointing to the file
        :type file: Path
        """
        self.file = file
        self.size = file.stat().st_size
        self._md5 = None

    @property
    def name(self) -> str:
        """
        Returns file name
        """
        return self.file.name

    def _calculate_md5(self) -> str:
        """
        TODO
        """
        hash_md5 = md5()
        with open(self.file.as_posix(), 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        self._md5 = hash_md5.hexdigest()
        return self._md5

    def get_hash(self) -> str:
        """
        TODO
        :return:
        """
        if self._md5 is None:
            return self._calculate_md5()
        else:
            return self._md5

    def compare_to(self, file: 'File') -> bool:
        """
        TODO
        :param file:
        :return:
        """
        if self.size != file.size:
            return False
        else:
            return self.get_hash() == file.get_hash()
