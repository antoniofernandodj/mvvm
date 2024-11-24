import base64
import httpx

class FileClient:
    def __init__(self, base_url: str):
        self.client = httpx.Client(base_url=base_url)

    def download_file(self, file_id: str):
        return self.client.stream("GET", f"/file/download/{file_id}")

    def rename_file(self, file_id: str, new_name: str) -> httpx.Response:
        return self.client.patch(f"/file/rename/{file_id}", params={"new_filename": new_name})

    def delete_file(self, file_id: str) -> httpx.Response:
        return self.client.delete(f"/file/{file_id}")

    def list_directory(self, path: str) -> httpx.Response:
        return self.client.get("/directory/tree/", params={"path": path})

    def create_directory(self, path: str) -> httpx.Response:
        return self.client.post("/directory/create/", params={"path": path})

    def delete_directory(self, path: str) -> httpx.Response:
        return self.client.delete("/directory/delete/", params={"path": path})
    
    def rename_directory(self, path: str, new_directory_path: str) -> httpx.Response:
        params = {"path": path, 'new_directory_path': new_directory_path}
        return self.client.patch("/directory/rename/", params=params)
    
    def store_file(self, path: str, file_name: str, data: bytes) -> httpx.Response:
        body = {"name": file_name, 'b64': base64.b64encode(data).decode('utf-8')}
        return self.client.post("/file/store/", json=body, params={'path': path})
    
    def move_file(self, path: str, file_name: str, new_directory_path: str) -> httpx.Response:
        params = {"filename": file_name, 'path': path, 'new_directory_path': new_directory_path}
        return self.client.put("/file/move/", params=params)
    
    def move_directory(self, path: str, new_directory_path: str) -> httpx.Response:
        params = {'path': path, 'new_parent_path': new_directory_path}
        return self.client.put("/directory/move/", params=params)
    
    def copy_file(self, path: str, file_name: str, new_directory_path: str) -> httpx.Response:
        params = {"filename": file_name, 'path': path, 'new_directory_path': new_directory_path}
        return self.client.post("/file/copy/", params=params)