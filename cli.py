"""
Console line interface
"""
from pathlib import Path

import click

from dupe import FileBank


# noinspection PyMissingOrEmptyDocstring
@click.group()
def cli(): pass


@cli.command()
@click.argument('folder')
def look_duplicates(folder: str):
    """
    Search the folder and subfolders for duplicate files.


    :param folder: String of the folder name
    """
    files = FileBank(folder)
    files.print_duplicates()


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
def look_duplicates_save(folder: str):
    """
    Looks for duplicate files in the folder and subfolders.
    Prints the results and creates a json file.

    :param folder: String of the folder name.
    """
    if not Path(folder).is_dir():
        print('Folder does not exist')
        exit()
    files = FileBank(folder)
    files.print_duplicates()
    files.save_json()


if __name__ == '__main__':
    cli()
