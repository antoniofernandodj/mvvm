from typing import List, Optional

from config import download_stream_data
from .tree import Ui_MainWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu, QTreeView, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from pathlib import Path
import httpx


class TreeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selected_item: Optional[dict] = None

        # Configurações ou sinais adicionais podem ser feitos aqui
        self.setup_tree_view()

    def on_item_clicked(self, index):
        """
        Método chamado quando um item é clicado na árvore.
        """
        item = self.model.itemFromIndex(index)
        file_data = item.data()

        title: str = "Download"
        question: str = f"Você deseja realizar o donwload do arquivo {file_data['nome']}?"
        result = QMessageBox.question(self, title, question)
        if result != QMessageBox.StandardButton.Yes:
            return

        url = f'http://localhost:8000/file/download/{file_data['id']}'
        with httpx.stream('GET', url) as response:
            try:
                download_stream_data(filename=file_data['nome'], stream_response=response)
            except:
                title: str = 'Erro no download'
                msg: str = f"Falha ao baixar o arquivo {file_data['nome']}."
                QMessageBox.warning(self, title, msg)
        
        title: str = 'Download Completo'
        msg: str = f'Arquivo {file_data['nome']} baixado com sucesso!'
        QMessageBox.information(self, title, msg)

    def setup_tree_view(self):
        """
        Configurações adicionais para o QTreeView ou para carregar dados nele.
        """
        # Exemplo: alterando o cabeçalho ou configurando os itens

        self.model = QStandardItemModel()

        response = httpx.get('http://localhost:8000/directory/tree/')
        data = response.json()

        self.ui.treeView.setHeaderHidden(False)
        self.ui.treeView.setAlternatingRowColors(True)

        # self.ui.treeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.ui.treeView.customContextMenuRequested.connect(self.show_context_menu)


        def mount(
            data,
            parent: Optional[QStandardItem] = None,
            result: List[QStandardItem] = []
        ) -> List[QStandardItem]:
            """
            Função recursiva para construir a árvore de diretórios e arquivos.
            """

            for file in data['files']:
                item = QStandardItem(file['nome'])
                item.setData(file)
                if parent is None:
                    self.model.appendRow(item)
                else:
                    parent.appendRow(item)
 
            if len(data['subdirectories']) == 0:
                return result

            for dirt in data['subdirectories']:
                path = Path(dirt['path'])
                dir_item = QStandardItem(path.name)
                dir_item.setData(dirt)
                if parent is None:
                    self.model.appendRow(dir_item)
                else:
                    parent.appendRow(dir_item)

                mount(data=dirt, parent=dir_item, result=result)

            return result


        result = mount(data)

        self.model.appendRow(result)

        self.ui.treeView.setModel(self.model)
        self.ui.treeView.doubleClicked.connect(self.on_item_clicked)
        # self.ui.treeView.clicked.connect(self.on_item_clicked)

    def show_context_menu(self, pos):
        """
        Mostra um menu de contexto quando o botão direito é clicado
        """
        # Cria o menu de contexto
        menu = QMenu(self)

        print(pos)

        # Adiciona ações ao menu
        action_open = QAction("Abrir", self)
        action_open.triggered.connect(self.on_open_action)

        action_delete = QAction("Deletar", self)
        action_delete.triggered.connect(self.on_delete_action)

        # Adiciona as ações ao menu
        menu.addAction(action_open)
        menu.addAction(action_delete)

        # Exibe o menu de contexto
        menu.exec(self.ui.treeView.viewport().mapToGlobal(pos))

    def on_open_action(self, x):
        print(f"Abrir item {x}")

    def on_delete_action(self, x):
        print(f"Deletar item {x}")