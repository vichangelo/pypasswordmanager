import os

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data_folder() -> str:
    return os.path.join(_ROOT, "data/")


def get_file_path(filename: str):
    return os.path.join(get_data_folder(), filename)
