import os
from typing import List, Optional, TypedDict
from httpx import Response
from PySide6.QtGui import QStandardItem, QStandardItemModel, QIcon
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QSettings
from pathlib import Path


# Defina o escopo e a organização
settings = QSettings(
    "settings.ini",
    QSettings.Format.IniFormat
)


class Favorito(TypedDict):
    id: str
    nome: str
    tamanho: int
    path: str


class FavoritosService:
    def __init__(self, settings: QSettings):
        self.settings = settings

    def add(self, item: Favorito) -> None:
        favoritos = self.get_all()
        if item not in favoritos:  # Evita duplicatas
            favoritos.append(item)
            self.settings.setValue('favoritos', favoritos)
            self.settings.sync()

    def get_all(self) -> List[Favorito]:
        return self.settings.value('favoritos', type=list)  # type: ignore

    def remove(self, item: str) -> None:
        favoritos = self.get_all()
        if item in favoritos:
            favoritos.remove(item)
            self.settings.setValue('favoritos', favoritos)
            self.settings.sync()


def download_stream_data(filename: str, stream_response: Response):
    download_path = str(settings.value('download_path', defaultValue='', type=str))
    complete_file_path = os.path.join(download_path, filename)
    if stream_response.status_code != 200:
        raise ConnectionError(stream_response.content.decode('utf-8'))

    try:
        with open(complete_file_path, 'wb') as f:
            data: bytes
            for data in stream_response.iter_bytes():
                f.write(data)
    except:
        raise ConnectionError(stream_response.content.decode('utf-8'))


def create_file(data, name):
    item = QStandardItem(data['nome'])
    item.setData(data)
    item.setEditable(False)
    return item

def create_dir(data):
    # item = QStandardItem(data['nome'])
    # item.setData(data)
    # item.setEditable(False)
    # return item
    path = Path(data['path'])
    dir_item = QStandardItem(path.name)
    dir_item.setData(data)
    dir_item.setEditable(False)
    return dir_item

def mount(
    data,
    model: Optional[QStandardItemModel],
    parent: Optional[QStandardItem] = None,
    result: List[QStandardItem] = []
) -> List[QStandardItem]:
    """
    Função recursiva para construir a árvore de diretórios e arquivos.
    """
    try:
        for file in data['files']:
            item = create_file(file, file['nome'])
            item.setIcon(QIcon('icons/file2.png'))
            item.setData(file)
            if parent is None and model is not None:
                model.appendRow(item)
            if parent is not None and model is None:
                parent.appendRow(item)

        for dirt in data['subdirectories']:
            dir_item = create_dir(dirt)
            dir_item.setData(dirt)
            dir_item.setIcon(QIcon('icons/folder2.png'))
            if parent is None and model is not None:
                model.appendRow(dir_item)
            if parent is not None and model is None:
                parent.appendRow(dir_item)

            mount(
                data=dirt,
                model=None,
                parent=dir_item,
                result=result
            )

        return result
    except:
        print(data)
        raise


def ensure_slash_after_and_before(path: str):
    path = '/' + path if not path.startswith('/') else path
    path = path + '/' if not path.endswith('/') else path
    return path
