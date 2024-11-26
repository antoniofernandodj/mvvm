from __future__ import annotations
from ctypes import Union
from typing import List, Optional, TypedDict


class FileDict(TypedDict):
    id: str
    nome: str
    tamanho: int

class DirectoryDict(TypedDict):
    path: str
    files: List[FileDict]
    subdirectories: List[DirectoryDict]

class FileOrDirDict(FileDict, DirectoryDict):
    mode: Optional[str]
