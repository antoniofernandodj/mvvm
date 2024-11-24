from __future__ import annotations
import os
from typing import Literal
from config import ensure_slash_after_and_before, mount, settings
from context_menu import ContextMenu, is_file
from file_operations import FileOperations
from network import FileClient
from .tree import Ui_MainWindow
from PySide6.QtCore import QSize, Qt, QPoint, QModelIndex
from PySide6.QtWidgets import QListView, QMainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QStandardItemModel
from pathlib import Path


class FileMongo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__copy_from_data = None
        self.settings = settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_path = '/'
        self.copy_from_data = None
        self.setWindowTitle('FileMongo')
        self.model = QStandardItemModel()
        self.model_tree = QStandardItemModel()
        self.client = FileClient(base_url=self.settings.value('API'))
        self.file_operations = FileOperations(self, self.client)
        self.context_menu = ContextMenu(self, self.file_operations)
        self.setup_tree_view()
        self.setup_callbacks()

    def voltar(self):
        parent_path = str(Path(self.current_path).parent)
        self.mount_on_path(parent_path)

    def enter_directory_from_address_bar(self):
        path = self.ui.lineEdit.text()
        self.mount_on_path(path)

    def on_item_clicked(self, index: QModelIndex):
        item = self.model.itemFromIndex(index)
        file_data = item.data()
        self.open_or_download(file_data=file_data)

    def open_or_download(self, file_data: dict):
        if is_file(file_data):
            self.file_operations.download_file(file_data)

        if not is_file(file_data):
            self.mount_on_path(file_data['path'])

    def mount_on_path(self, path: str):
        path = ensure_slash_after_and_before(path)
        data = self.file_operations.list_directory(path)

        if 'não encontrado' in str(data):
            title: str = 'Erro na busca'
            text = f'Diretório {path} não encontrado. Deseja criar?'
            result = QMessageBox.question(
                self, title, text,
                QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes
            )

            if result != QMessageBox.StandardButton.Yes.value:
                return
            
            self.file_operations.create_directory(path)
            self.open_or_download({'path': path})
            return

        self.model.clear()
        self.model.appendRow(mount(data, self.model))
        self.ui.lineEdit.setText(path)
        self.current_path = path

    def setup_tree_view(self):
        self.ui.listView.setModel(self.model)
        self.ui.listView.setSpacing(27)
        self.ui.treeView.setModel(self.model_tree)

        self.ui.listView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.listView.customContextMenuRequested.connect(self.show_context_menu)

        self.ui.aux_label.setVisible(False)
        self.ui.colar_aqui_button.setVisible(False)

        self.mount_on_path('/')

        data = self.file_operations.list_directory('/')
        self.model_tree.appendRow(mount(data, self.model_tree))

        self.ui.listView.setViewMode(QListView.ViewMode.IconMode)
        self.ui.listView.setIconSize(QSize(64,64))
        self.ui.listView.doubleClicked.connect(self.on_item_clicked)

    def show_context_menu(self, pos: QPoint):
        index = self.ui.listView.indexAt(pos)
        if not index.isValid():
            return

        item = self.model.itemFromIndex(index)
        file_data = item.data()

        menu = self.context_menu.create_menu(file_data=file_data)
        menu.exec(self.ui.listView.viewport().mapToGlobal(pos))

    def refresh_dirs(self):
        self.mount_on_path(self.current_path)

        self.model_tree.clear()
        data = self.file_operations.list_directory('/')
        self.model_tree.appendRow(mount(data, self.model_tree))

    def set_copy_from_file_data(self, file_data: dict, mode: Literal['move', 'copy']):

        complete_path = None
        if is_file(file_data):
            complete_path = os.path.join(self.current_path, file_data['nome'])
            file_data = file_data | {'path': self.current_path, 'mode': mode}
            self.__copy_from_data = file_data | {'path': self.current_path, 'mode': mode, 'type': 'file'}
        else:
            complete_path = file_data['path']
            self.__copy_from_data = file_data | {'path': complete_path, 'mode': mode, 'type': 'directory'}

        
        self.ui.aux_label.setText('Copied:' if mode == 'copy' else 'Cut:')
        self.ui.aux_label.setVisible(True)
        self.ui.colar_aqui_button.setVisible(True)
        self.ui.cutted_label.setVisible(True)

        if is_file(file_data) and complete_path:
            self.ui.cutted_label.setText(complete_path)
        elif not is_file(file_data) and complete_path:
            self.ui.cutted_label.setText(complete_path)

    def paste_here(self):
        if self.__copy_from_data is None:
            raise ValueError

        if self.__copy_from_data['mode'] == 'move':
            self.file_operations.move(self.__copy_from_data, self.current_path)
            self.ui.aux_label.setVisible(False)
            self.ui.colar_aqui_button.setVisible(False)
            self.ui.cutted_label.setVisible(False)
            self.__copy_from_data = None

        elif self.__copy_from_data['mode'] == 'copy':
            self.file_operations.copy_file(
                self.__copy_from_data['path'],
                self.__copy_from_data['nome'],
                self.current_path
            )
        else:
            raise ValueError('Modo inválido')

    def clear_labels_if_deleted(self, id: str):
        data = self.__copy_from_data
        if data is None:
            raise ValueError
        
        if data['id'] != id:
            return

        self.ui.aux_label.setVisible(False)
        self.ui.colar_aqui_button.setVisible(False)
        self.ui.cutted_label.setVisible(False)
        self.__copy_from_data = None

    def clear_copy_from_data_if_file_not_exists_anymore(self, file_data):
        data = self.__copy_from_data
        if data is None:
            return

        if file_data['id'] == data['id']:
            self.ui.aux_label.setVisible(False)
            self.ui.colar_aqui_button.setVisible(False)
            self.ui.cutted_label.setVisible(False)
            self.__copy_from_data = None

    def setup_callbacks(self):
        f = self.enter_directory_from_address_bar
        self.ui.ir_button.clicked.connect(f)
        self.ui.lineEdit.returnPressed.connect(f)

        f = self.voltar
        self.ui.voltar_button.clicked.connect(f)

        f = self.file_operations.nova_pasta
        self.ui.nova_pasta.clicked.connect(f)

        f = self.file_operations.file_store
        self.ui.upload_button.clicked.connect(f)

        f = self.paste_here
        self.ui.colar_aqui_button.clicked.connect(f)
