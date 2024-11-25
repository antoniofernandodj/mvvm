from config import Favorito
from typing import Union


def is_file(file_data: Union[dict, Favorito]) -> bool:
    return file_data.get('nome') is not None