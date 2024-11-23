from httpx import Response
from pathlib import Path
import os



class Settings:
    path: str = os.path.join(
        str(Path(__file__).parent.resolve()),
        "download"
    )


def download_stream_data(filename: str, stream_response: Response):
    complete_file_path = os.path.join(Settings.path, filename)
    if stream_response.status_code != 200:
        raise ConnectionError(stream_response.content.decode('utf-8'))

    try:
        with open(complete_file_path, 'wb') as f:
            data: bytes
            for data in stream_response.iter_bytes():
                f.write(data)
    except:
        raise ConnectionError(stream_response.content.decode('utf-8'))
