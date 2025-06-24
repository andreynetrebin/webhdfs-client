from api_tool import RestApiTool
from typing import Optional, Union, Dict, Any

class WebHDFSClient:
    def __init__(self, base_url: str, username: str = None, auth_token: str = None):
        """
        Инициализация клиента WebHDFS

        :param base_url: Базовый URL WebHDFS (например: http://namenode:50070/webhdfs/v1)
        :param username: Имя пользователя Hadoop
        :param auth_token: Токен аутентификации (если требуется)
        """
        self.api = RestApiTool(base_url.rstrip('/'), token=auth_token)
        self.username = username
        self.default_params = {}
        if username:
            self.default_params['user.name'] = username

    def _merge_params(self, params: Dict = None) -> Dict:
        """Объединение параметров запроса с параметрами по умолчанию"""
        if params is None:
            return self.default_params.copy()
        return {**self.default_params, **params}

    def list_status(self, path: str) -> Dict:
        """Получить список файлов в директории"""
        params = self._merge_params({'op': 'LISTSTATUS'})
        return self.api.get(path, params=params)

    def get_file_status(self, path: str) -> Dict:
        """Получить информацию о файле/директории"""
        params = self._merge_params({'op': 'GETFILESTATUS'})
        return self.api.get(path, params=params)

    def mkdirs(self, path: str, permission: str = '755') -> bool:
        """Создать директорию(и) на HDFS"""
        params = self._merge_params({
            'op': 'MKDIRS',
            'permission': permission
        })
        response = self.api.put(path, params=params)
        return response.get('boolean', False)

    def read_file(self, path: str, offset: int = 0, length: int = None) -> Union[str, bytes]:
        """Чтение файла с HDFS"""
        params = self._merge_params({'op': 'OPEN'})
        if offset > 0:
            params['offset'] = offset
        if length:
            params['length'] = length

        response = self.api.get(path, params=params)
        return response

    def upload_file(self, local_path: str, hdfs_path: str, overwrite: bool = True,
                    replication: int = None, blocksize: int = None, permission: str = None) -> bool:
        """Загрузка файла на HDFS"""
        replication = str(replication) if replication is not None else None
        blocksize = str(blocksize) if blocksize is not None else None

        params = self._merge_params({
            'op': 'CREATE',
            'overwrite': str(overwrite).lower()
        })
        if replication:
            params['replication'] = replication
        if blocksize:
            params['blocksize'] = blocksize
        if permission:
            params['permission'] = permission

        response = self.api.put(hdfs_path, params=params, headers={'Content-Type': 'application/octet-stream'})

        if response and 'Location' in response:
            with open(local_path, 'rb') as f:
                upload_url = response['Location']
                result = self.api.put('', full_url=upload_url, data=f.read())
                return True

        return False

    def append_to_file(self, local_path: str, hdfs_path: str, buffersize: int = None) -> bool:
        """Добавление данных в существующий файл на HDFS"""
        params = self._merge_params({'op': 'APPEND'})
        if buffersize:
            params['buffersize'] = str(buffersize)

        response = self.api.post(hdfs_path, params=params)

        if response and 'Location' in response:
            with open(local_path, 'rb') as f:
                append_url = response['Location']
                self.api.post('', full_url=append_url, data=f.read())
                return True

        return False

    def delete_file(self, path: str, recursive: bool = False) -> bool:
        """Удаление файла/директории"""
        params = self._merge_params({
            'op': 'DELETE',
            'recursive': str(recursive).lower()
        })
        response = self.api.delete(path, params=params)
        return response.get('boolean', False)

    def rename_file(self, src_path: str, dst_path: str) -> bool:
        """Переименование/перемещение файла"""
        params = self._merge_params({
            'op': 'RENAME',
            'destination': dst_path
        })
        response = self.api.put(src_path, params=params)
        return response.get('boolean', False)

    def get_content_summary(self, path: str) -> Dict:
        """Получить статистику по содержимому"""
        params = self._merge_params({'op': 'GETCONTENTSUMMARY'})
        return self.api.get(path, params=params)

    def get_checksum(self, path: str) -> Dict:
        """Получить контрольную сумму файла"""
        params = self._merge_params({'op': 'GETFILECHECKSUM'})
        return self.api.get(path, params=params)
