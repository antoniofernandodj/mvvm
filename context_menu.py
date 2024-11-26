# context_menu.py
from contextlib import suppress
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from file_operations import FileOperations
from t import FileOrDirDict
from utils import is_file
from config import settings, FavoritosService

with suppress(Exception):
    from view import FileMongo


class ContextMenu:
    def __init__(self, window: 'FileMongo', file_operations: FileOperations):
        self.window = window
        self.file_operations = file_operations
        self.favoritos = FavoritosService(settings)

    def create_file_menu(self, file_data: FileOrDirDict) -> QMenu:
        menu = QMenu(self.window)

        menu.addAction(self.create_action_open(data=file_data))
        menu.addAction(self.create_action_delete(data=file_data))
        menu.addAction(self.create_action_rename(data=file_data))
        menu.addAction(self.create_action_move(data=file_data))
        menu.addAction(self.create_action_add_bookmark(data=file_data))
        if is_file(file_data):
            menu.addAction(self.create_action_copy(data=file_data))
        else:
            menu.addAction(self.create_action_folder_properties(path=file_data['path']))
        menu.addAction(QAction("Fechar", self.window))

        return menu
    
    def create_folder_menu(self, path):
        menu = QMenu(self.window)

        menu.addAction(self.create_action_new_folder(path=path))
        menu.addAction(self.create_action_folder_properties(path=path))
        menu.addAction(self.create_action_paste_here())

        return menu
    

    def create_action_new_folder(self, path):
        action = QAction('Nova pasta', self.window)
        action.triggered.connect(lambda: self.file_operations.nova_pasta(path))
        return action

    def create_action_folder_properties(self, path):
        action = QAction('Propriedades', self.window)
        action.triggered.connect(lambda: self.file_operations.get_properties_stream(path))
        return action

    def create_action_paste_here(self):
        action = QAction('Colar aqui', self.window)
        if self.window.copy_from_data is None:
            action.setEnabled(False)

        action.triggered.connect(lambda: self.window.paste_here())
        return action


    def create_favoritos_menu(self, file_data):
        menu = QMenu(self.window)
        menu.addAction(self.create_action_open(data=file_data))
        menu.addAction(self.create_action_remove_bookmark_remove(data=file_data))
        menu.addAction(self.create_action_open_parent(data=file_data))

        return menu

    def create_action_open_parent(self, data):
        if is_file(data):
            action_open_parent_title = "Abrir localização de arquivo"
        else:
            action_open_parent_title = "Abrir localização de diretório"
        action_open_parent = QAction(action_open_parent_title, self.window)
        action_open_parent.triggered.connect(lambda: self.window.open_parent(data))
        return action_open_parent

    def create_action_remove_bookmark_remove(self, data):
        action_remove_favorito = QAction('Remover favorito', self.window)

        def remove_bookmark(context_menu: ContextMenu):
            context_menu.favoritos.remove(data)
            context_menu.window.mount_favoritos()

        action_remove_favorito.triggered.connect(lambda: remove_bookmark(self))
        return action_remove_favorito

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
        print(data)
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

    def create_action_add_bookmark(self, data):
        action_add_bookmark = QAction("Adicionar aos favoritos", self.window)

        def add_bookmark(context_menu: ContextMenu):
            context_menu.favoritos.add(data)
            context_menu.window.mount_favoritos()

        action_add_bookmark.triggered.connect(lambda: add_bookmark(self))
        return action_add_bookmark
