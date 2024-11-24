# file_operations.py
from contextlib import suppress
import os
from pathlib import Path
from PySide6.QtWidgets import QMessageBox, QInputDialog, QFileDialog
from config import download_stream_data, ensure_slash_after_and_before
from utils import is_file
from network import FileClient


with suppress(ImportError, ModuleNotFoundError):
    from view import FileMongo


class FileOperations:
    def __init__(self, window: 'FileMongo', client: FileClient):
        self.window = window
        self.client = client

    def download_file(self, file_data: dict):
        title = "Download"
        question = f"Você deseja realizar o download do arquivo {file_data['nome']}?"
        if QMessageBox.question(self.window, title, question) != QMessageBox.StandardButton.Yes:
            return
        try:
            with self.client.download_file(file_data["id"]) as response:
                download_stream_data(filename=file_data["nome"], stream_response=response)
            QMessageBox.information(
                self.window,
                "Download Completo",
                f"Arquivo {file_data['nome']} baixado com sucesso!"
            )
        except Exception as e:
            QMessageBox.warning(
                self.window,
                "Erro no Download",
                f"Falha ao baixar o arquivo {file_data['nome']}: {e}"
            )

    def rename(self, file_data: dict):
        if is_file(file_data):
            self.rename_file(file_data)
        else:
            self.rename_directory(file_data)

    def delete(self, file_data: dict):
        if is_file(file_data):
            self.delete_file(file_data)
        else:
            self.delete_directory(file_data)

    def rename_file(self, file_data: dict):
        title = "Rename"
        label = "Digite o novo nome de arquivo:"
        new_name, ok = QInputDialog.getText(self.window, title, label, text=file_data["nome"])
        if not ok:
            return
        new_name = new_name.strip()
        try:
            self.client.rename_file(file_data["id"], new_name)
            QMessageBox.information(
                self.window,
                "Sucesso",
                f"Arquivo {new_name} renomeado com sucesso!"
            )
        except Exception as e:
            QMessageBox.warning(
                self.window,
                "Erro na operação",
                f"Falha ao renomear o arquivo {file_data['nome']}: {e}"
            )

        self.window.refresh_dirs()

    def rename_directory(self, file_data: dict):
        title: str = "Rename"
        label: str = "Digite o novo nome do diretório:"
        path = Path(file_data["path"]).name
        new_name, ok = QInputDialog.getText(self.window, title, label, text=path)
        if not ok:
            return
        new_name = new_name.strip()
        path = file_data['path']
        new_directory_path = ensure_slash_after_and_before(
            os.path.join(str(Path(path).parent), new_name)
        )
        try:
            self.client.rename_directory(file_data["path"], new_directory_path)
            QMessageBox.information(
                self.window,
                "Sucesso",
                f"Diretório {new_name} renomeado com sucesso!"
            )

        except Exception as e:
            QMessageBox.warning(
                self.window,
                "Erro na operação",
                f"Falha ao renomear o diretório {file_data['nome']}: {e}"
            )

        self.window.refresh_dirs()

    def delete_directory(self, file_data: dict):
        title: str = "Remove"
        question: str = f"Você deseja remover o diretório {file_data['path']}?"

        result = QMessageBox.warning(
            self.window, title,
            question,
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )

        if result != QMessageBox.StandardButton.Yes.value:
            return

        path_name = Path(file_data['path']).name
        response = self.client.delete_directory(file_data['path'])
        try:
            response.raise_for_status()
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao remover o diretório {path_name}: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return
        
        title: str = 'Sucesso'
        msg: str = f'Diretório {path_name} removido com sucesso!'
        QMessageBox.information(self.window, title, msg)
        self.window.refresh_dirs()

    def move(self, file_data: dict, new_parent_path: str):
        if is_file(file_data):
            self.move_file(file_data['path'], file_data['nome'], new_parent_path)
        else:
            self.move_directory(file_data['path'], new_parent_path)

    def move_file(self, path: str, filename: str, new_directory_path: str):
        try:
            response = self.client.move_file(path, filename, new_directory_path)
            response.raise_for_status()
            title: str = 'Sucesso'
            msg: str = f'Arquivo {filename} movido com sucesso!'
            QMessageBox.information(self.window, title, msg)
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao mover o arquivo: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return

        self.window.refresh_dirs()

    def move_directory(self, path: str, new_parent_path: str):
        try:
            response = self.client.move_directory(
                ensure_slash_after_and_before(path), 
                ensure_slash_after_and_before(new_parent_path)
            )
            response.raise_for_status()
            title: str = 'Sucesso'
            msg: str = f'Diretório {path} movido com sucesso!'
            QMessageBox.information(self.window, title, msg)
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao mover o diretório: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return

        self.window.refresh_dirs()

    def copy_file(self, path: str, filename: str, new_directory_path: str):
        try:
            response = self.client.copy_file(path, filename, new_directory_path)
            response.raise_for_status()
            title: str = 'Sucesso'
            msg: str = f'Arquivo {filename} copiado com sucesso!'
            QMessageBox.information(self.window, title, msg)
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao copiar o arquivo: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return

        self.window.refresh_dirs()

    def nova_pasta(self):
        title: str = 'Nova pasta'
        label: str = 'Digite o nome da nova pasta'
        text, ok = QInputDialog.getText(self.window, title, label)
        if not ok:
            return
        text = text.strip()
        path = os.path.join(self.window.current_path, text)
        
        response = self.client.create_directory(path)
        try:
            response.raise_for_status()
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao criar o diretório {text}: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return
        
        title: str = 'Sucesso'
        msg: str = f'Diretório {text} criado com sucesso!'
        QMessageBox.information(self.window, title, msg)

        self.window.refresh_dirs()

    def create_directory(self, path):
        response = self.client.create_directory(path)
        try:
            response.raise_for_status()
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao criar o diretório {path}: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return
        
        title: str = 'Sucesso'
        msg: str = f'Diretório {path} criado com sucesso!'
        QMessageBox.information(self.window, title, msg)

        self.window.refresh_dirs()

    def delete_file(self, file_data: dict):
        title: str = "Remove"
        question: str = f"Você deseja remover o arquivo {file_data['nome']}?"
        result = QMessageBox.warning(
            self.window, title,
            question,
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )
        if result != QMessageBox.StandardButton.Yes:
            return

        response = self.client.delete_file(file_data['id'])
        try:
            response.raise_for_status()
        except Exception as erro:
            title: str = 'Erro na operação'
            msg: str = f"Falha ao remover o arquivo {file_data['nome']}: {erro}"
            QMessageBox.warning(self.window, title, msg)
            return
        
        title: str = 'Sucesso'
        msg: str = f'Arquivo {file_data['nome']} removido com sucesso!'
        QMessageBox.information(self.window, title, msg)
        self.window.refresh_dirs()
        self.window.clear_copy_from_data_if_file_not_exists_anymore(file_data)

    def list_directory(self, path: str):
        path = ensure_slash_after_and_before(path)
        response = self.client.list_directory(path)
        
        try:
            return response.json()
        except BaseException:
            print(response)
            print(response.content)
            raise
    
    def file_store(self):
        filepath_input, _ = QFileDialog.getOpenFileName(
            self.window, "Selecionar arquivo para upload",
            os.getcwd(), "Todos os Arquivos (*.*)"
        )
        if not filepath_input:
            return

        filename = Path(filepath_input).name
        filepath_output = self.window.current_path
        try:
            with open(filepath_input, 'rb') as f:
                response = self.client.store_file(filepath_output, filename, f.read())
                response.raise_for_status()

            QMessageBox.information(
                self.window, "Sucesso",
                f"Arquivo enviado para {filepath_output} com sucesso!"
            )
            self.window.refresh_dirs()

        except Exception as erro:
            QMessageBox.warning(self.window, "Erro", f"Falha ao enviar o arquivo: {erro}")
