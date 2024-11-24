# context_menu.py
from contextlib import suppress
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from file_operations import FileOperations
from utils import is_file

with suppress(Exception):
    from view import FileMongo


class ContextMenu:
    def __init__(self, window: 'FileMongo', file_operations: FileOperations):
        self.window = window
        self.file_operations = file_operations

    def create_menu(self, file_data: dict) -> QMenu:
        menu = QMenu(self.window)

        menu.addAction(self.create_action_open(data=file_data))
        menu.addAction(self.create_action_delete(data=file_data))
        menu.addAction(self.create_action_rename(data=file_data))
        menu.addAction(self.create_action_move(data=file_data))
        if is_file(file_data):
            menu.addAction(self.create_action_copy(data=file_data))
        menu.addAction(QAction("Fechar", self.window))

        return menu

    def create_action_open(self, data):
        action_open_title = "Download" if is_file(data) else "Abrir"
        action_open = QAction(action_open_title, self.window)
        action_open.triggered.connect(
            lambda: self.file_operations.download_file(data) if is_file(data)
            else self.window.open_or_download(data)
        )

        return action_open

    def create_action_delete(self, data):
        action_delete = QAction("Deletar", self.window)
        action_delete.triggered.connect(lambda: self.file_operations.delete(data))
        return action_delete
    
    def create_action_rename(self, data):
        action_rename = QAction("Renomear", self.window)
        action_rename.triggered.connect(lambda: self.file_operations.rename(data))
        return action_rename
    
    def create_action_move(self, data):
        action_cut = QAction("Recortar", self.window)
        action_cut.triggered.connect(lambda: self.window.set_copy_from_file_data(data, 'move'))
        return action_cut
    
    def create_action_copy(self, data):
        action_copy = QAction("Copiar", self.window)
        action_copy.triggered.connect(lambda: self.window.set_copy_from_file_data(data, 'copy'))
        return action_copy
