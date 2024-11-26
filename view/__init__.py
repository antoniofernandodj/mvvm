from __future__ import annotations

import os
from typing import Literal, Optional
from pathlib import Path

from PySide6.QtCore import (
    QSize,
    Qt,
    QPoint,
    QModelIndex,
    QThread,
    Signal,
    QEvent
)
from PySide6.QtWidgets import (
    QListView, QMainWindow,
    QStyledItemDelegate,
    QMessageBox,
    QFileDialog
)
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QResizeEvent,
    QMoveEvent,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QBrush,
    QColor
)
from config import (
    FavoritosService,
    ensure_slash_after_and_before,
    mount,
    settings
)
from context_menu import ContextMenu
from utils import is_file
from file_operations import FileOperations
from network import FileClient
from .tree import Ui_MainWindow



class FileMongo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_path = '/'
        self.copy_from_data = None
        self.setWindowTitle('FileMongo')
        self.file_view_model = QStandardItemModel()
        self.model_tree = QStandardItemModel()
        self.favoritos_model = QStandardItemModel()
        self.client = FileClient(base_url=self.settings.value('API'))
        self.file_operations = FileOperations(self, self.client)
        self.context_menu = ContextMenu(self, self.file_operations)
        self.favoritos = FavoritosService(self.settings)
        self.setMinimumWidth(100)
        self.item_from: Optional[QStandardItem] = None
        self.item_to: Optional[QStandardItem] = None

        self.restore_window_position()

        self.setup_tree_view()
        self.setup_callbacks()

    def voltar(self):
        parent_path = str(Path(self.current_path).parent)
        self.mount_on_path(parent_path)

    def enter_directory_from_address_bar(self):
        path = self.ui.lineEdit.text()
        self.mount_on_path(path)

    def on_item_clicked(self, index: QModelIndex):
        item = self.file_view_model.itemFromIndex(index)
        file_data = item.data()
        self.open_or_download(file_data=file_data)

    def on_bookmark_clicked(self, index: QModelIndex):
        item = self.favoritos_model.itemFromIndex(index)
        file_data = item.data()
        self.open_or_download(file_data=file_data)

    def on_item_tree_clicked(self, index: QModelIndex):
        item = self.model_tree.itemFromIndex(index)
        file_data = item.data()
        self.open_or_download(file_data=file_data)

    def open_or_download(self, file_data: dict):
        if is_file(file_data):
            self.file_operations.download_file(file_data)

        if not is_file(file_data):
            self.mount_on_path(file_data['path'])

    def open_parent(self, file_data: dict):
        if is_file(file_data):
            response = self.client.get_file_info(file_data['id'])
            file_data = response.json()
            self.mount_on_path(file_data['path'])
        else:
            response = self.client.get_dir_info(file_data['path'])
            file_data = response.json()
            parent_data = file_data.get('parent_data')
            if parent_data:
                self.mount_on_path(parent_data['path'])

    def mount_on_path(self, path: str, write=True):
        path = ensure_slash_after_and_before(path)
        data = self.file_operations.list_directory(path)
        model = self.file_view_model

        if 'não encontrado' in str(data):
            needs_confirmation = True if path != '/' else False

            if needs_confirmation:
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
            else:
                self.file_operations.create_directory(path, needs_confirmation)
                self.open_or_download({'path': path})
                return

        model.clear()
        model.appendRow(mount(data, model))
        self.ui.lineEdit.setText(path)
        self.current_path = path

        if write:
            self.settings.setValue('path', path)
            self.settings.sync()

    def setup_tree_view(self):
        self.ui.file_view.setModel(self.file_view_model)
        self.ui.file_view.setSpacing(27)
        self.ui.tree_view.setModel(self.model_tree)

        self.ui.aux_label.setVisible(False)
        self.ui.colar_aqui_button.setVisible(False)

        path = self.settings.value('path') or '/'
        self.mount_on_path(path, write=False)

        self.mount_favoritos()
        data = self.file_operations.list_directory('/')
        self.model_tree.appendRow(mount(data, self.model_tree))

        self.ui.file_view.setViewMode(QListView.ViewMode.IconMode)
        self.ui.file_view.setIconSize(QSize(64,64))
        self.ui.file_view.doubleClicked.connect(self.on_item_clicked)
        self.ui.file_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.file_view.customContextMenuRequested.connect(self.show_file_view_context_menu)

        self.ui.file_view.setDragEnabled(True)
        self.ui.file_view.setAcceptDrops(True)
        self.ui.file_view.setDragDropMode(QListView.DragDropMode.DragDrop)
        self.ui.file_view.installEventFilter(self)

        self.ui.file_view.dropEvent = self.drop_folder
        self.ui.file_view.dragEnterEvent = self.drag_foder_enter

        self.ui.tree_view.doubleClicked.connect(self.on_item_tree_clicked)
        self.ui.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tree_view.customContextMenuRequested.connect(self.show_tree_view_context_menu)

        self.ui.favoritos_tree_view.doubleClicked.connect(self.on_bookmark_clicked)
        self.ui.favoritos_tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.favoritos_tree_view.customContextMenuRequested.connect(
            self.show_favoritos_tree_view_context_menu
        )

    def drag_foder_enter(self, event: QDragMoveEvent):
        event.acceptProposedAction()

        index = self.ui.file_view.indexAt(event.pos())
        if index.isValid():
            self.item_from = self.file_view_model.itemFromIndex(index)


    def drop_folder(self, e: QDropEvent):
        e.setDropAction(Qt.DropAction.MoveAction)
        e.acceptProposedAction()

        index = self.ui.file_view.indexAt(e.pos())
        if index.isValid():

            self.item_to = self.file_view_model.itemFromIndex(index)
            if self.item_from is None:
                return
            if self.item_from == self.item_to:
                return

            item_from = self.item_from.data()
            item_to = self.item_to.data()
            item_from['type'] = 'file' if is_file(item_from) else 'directory'
            item_to['type'] = 'file' if is_file(item_to) else 'directory'

            if item_to['type'] == 'file':
                return
            
            from_path = self.current_path
            to_path = item_to['path']
            if item_from['type'] == 'directory':
                self.file_operations.move_directory(from_path, to_path)

            else:
                filename = item_from['nome']
                self.file_operations.move_file(from_path, filename, to_path)

            print({'to': item_to})
            print({'from': item_from})


    def show_favoritos_tree_view_context_menu(self, pos: QPoint):
        view = self.ui.favoritos_tree_view
        model = self.favoritos_model
        index = view.indexAt(pos)
        if not index.isValid():
            return

        item = model.itemFromIndex(index)
        file_data = item.data()

        menu = self.context_menu.create_favoritos_menu(file_data=file_data)
        menu.exec(view.viewport().mapToGlobal(pos))

    def show_file_view_context_menu(self, pos: QPoint):
        view = self.ui.file_view
        model = self.file_view_model
        index = view.indexAt(pos)
        if not index.isValid():
            menu = self.context_menu.create_folder_menu(path=self.current_path)
            menu.exec(view.viewport().mapToGlobal(pos))
            return

        item = model.itemFromIndex(index)
        file_data = item.data()

        menu = self.context_menu.create_file_menu(file_data=file_data)
        menu.exec(view.viewport().mapToGlobal(pos))

    def show_tree_view_context_menu(self, pos: QPoint):
        view = self.ui.tree_view
        model = self.model_tree
        index = view.indexAt(pos)
        if not index.isValid():
            return

        item = model.itemFromIndex(index)
        file_data = item.data()

        menu = self.context_menu.create_file_menu(file_data=file_data)
        menu.exec(view.viewport().mapToGlobal(pos))

    def mount_favoritos(self):

        self.favoritos_model.clear()
        for favorito in self.favoritos.get_all():
            if is_file(favorito):
                item = QStandardItem(favorito['nome'])
                item.setData(favorito)
                item.setEditable(False)
                self.favoritos_model.appendRow(item)
            else:
                item = QStandardItem(Path(favorito['path']).name)
                item.setData(favorito)
                item.setEditable(False)
                self.favoritos_model.appendRow(item)

            self.ui.favoritos_tree_view.setModel(self.favoritos_model)

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
            self.copy_from_data = file_data | {
                'path': self.current_path,
                'mode': mode,
                'type': 'file'
            }
        else:
            complete_path = file_data['path']
            self.copy_from_data = file_data | {
                'path': complete_path,
                'mode': mode, 'type':
                'directory'
            }

        
        self.ui.aux_label.setText('Copied:' if mode == 'copy' else 'Cut:')
        self.ui.aux_label.setVisible(True)
        self.ui.colar_aqui_button.setVisible(True)
        self.ui.cutted_label.setVisible(True)

        if is_file(file_data) and complete_path:
            self.ui.cutted_label.setText(complete_path)
        elif not is_file(file_data) and complete_path:
            self.ui.cutted_label.setText(complete_path)

    def paste_here(self):
        if self.copy_from_data is None:
            raise ValueError

        if self.copy_from_data['mode'] == 'move':
            self.file_operations.move(self.copy_from_data, self.current_path)
            self.ui.aux_label.setVisible(False)
            self.ui.colar_aqui_button.setVisible(False)
            self.ui.cutted_label.setVisible(False)
            self.copy_from_data = None

        elif self.copy_from_data['mode'] == 'copy':
            self.file_operations.copy_file(
                self.copy_from_data['path'],
                self.copy_from_data['nome'],
                self.current_path
            )
        else:
            raise ValueError('Modo inválido')

    def clear_labels_if_deleted(self, id: str):
        data = self.copy_from_data
        if data is None:
            raise ValueError
        
        if data['id'] != id:
            return

        self.ui.aux_label.setVisible(False)
        self.ui.colar_aqui_button.setVisible(False)
        self.ui.cutted_label.setVisible(False)
        self.copy_from_data = None

    def clear_copy_from_data_if_file_not_exists_anymore(self, file_data):
        data = self.copy_from_data
        if data is None:
            return

        if file_data['id'] == data['id']:
            self.ui.aux_label.setVisible(False)
            self.ui.colar_aqui_button.setVisible(False)
            self.ui.cutted_label.setVisible(False)
            self.copy_from_data = None

    def resizeEvent(self, event: QResizeEvent):

        def hide(*args):
            for arg in args:
                arg.setVisible(False)
        def show(*args):
            for arg in args:
                arg.setVisible(True)

        size = event.size()
        height = size.height()
        width = size.width()

        if width >= 600:
            show(self.ui.frame_4)
        else:
            hide(self.ui.frame_4)

        if height >= 460:
            show(self.ui.label, self.ui.favoritos_tree_view)
        else:
            hide(self.ui.favoritos_tree_view, self.ui.label)

    def closeEvent(self, event: QEvent):

        size = self.size()
    
        height = size.height()
        width = size.width()

        self.settings.setValue('width', width)
        self.settings.setValue('height', height)

        self.settings.sync()

    def restore_window_position(self):
        width: int = self.settings.value("width", 800, type=int)  # type: ignore
        height: int = self.settings.value("height", 600, type=int)  # type: ignore
        self.resize(width, height)


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
