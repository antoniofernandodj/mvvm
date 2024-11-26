from config import Favorito
from typing import Union

from t import DirectoryDict, FileDict


def is_file(file_data: Union[dict, Favorito, FileDict, DirectoryDict]) -> bool:
    return file_data.get('nome') is not None