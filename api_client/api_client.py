import requests
import logging
from typing import Optional, Dict, Any

class ApiError(Exception):
    """Custom exception for API errors"""
    pass

class RestApiTool:
    def __init__(self, base_url: str, token: Optional[str] = None,
                 enable_file_logging: bool = False, log_file_path: str = "api_tool.log"):
        """Initialize API client"""
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self._setup_logging(enable_file_logging, log_file_path)

    def _setup_logging(self, enable_file_logging: bool, log_file_path: str):
        """Настройка логирования"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Очистка предыдущих обработчиков
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Формат логов
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Обработчик для файла (если включено)
        if enable_file_logging:
            try:
                # Создаем директорию для логов если ее нет
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

                file_handler = logging.FileHandler(log_file_path)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

                self.logger.info(f"Логирование настроено в файл: {log_file_path}")
            except Exception as e:
                self.logger.error(f"Ошибка настройки файлового логирования: {str(e)}")

    def set_token(self, token: str):
        """Установить токен для аутентификации"""
        self.token = token
        self.logger.info("Токен установлен")

    def _get_headers(self, custom_headers: Optional[Dict] = None) -> Dict:
        """Формирование заголовков запроса"""
        headers = {'Accept': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для выполнения HTTP запросов"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(kwargs.pop('headers', None))

        self.logger.info(f"Отправка {method} запроса на {url}")
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)

            self.logger.info(f"Получен ответ: {response.status_code}")
            self.logger.debug(f"Заголовки запроса: {response.request.headers}")

            if 'data' in kwargs:
                self.logger.debug(f"Тело запроса: {str(kwargs['data'])[:500]}")
            elif 'json' in kwargs:
                self.logger.debug(f"JSON тело: {str(kwargs['json'])[:500]}")

            self.logger.debug(f"Тело ответа: {response.text[:500]}...")

            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при выполнении запроса: {str(e)}")
            raise ApiError(f"Ошибка сети: {str(e)}")

    def _handle_response(self, response: requests.Response) -> Union[Dict, str]:
        """Обработка ответа от сервера"""
        try:
            if response.status_code in range(200, 300):
                try:
                    return response.json()
                except ValueError:
                    return response.text
            else:
                error_msg = f"Ошибка {response.status_code}: {response.text}"
                self.logger.error(error_msg)
                raise ApiError(error_msg)
        except Exception as e:
            self.logger.error(f"Ошибка обработки ответа: {str(e)}")
            raise ApiError(f"Ошибка обработки ответа: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, **kwargs) -> Union[Dict, str]:
        """GET запрос"""
        response = self._make_request('GET', endpoint, params=params, headers=headers, **kwargs)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict] = None, **kwargs) -> Union[Dict, str]:
        """POST запрос"""
        response = self._make_request('POST', endpoint, json=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict] = None, **kwargs) -> Union[Dict, str]:
        """PUT запрос"""
        response = self._make_request('PUT', endpoint, json=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint: str, headers: Optional[Dict] = None, **kwargs) -> Union[Dict, str]:
        """DELETE запрос"""
        response = self._make_request('DELETE', endpoint, headers=headers, **kwargs)
        return self._handle_response(response)

    def upload_file(self, endpoint: str, file_path: str, field_name: str = 'file',
                    extra_data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Union[Dict, str]:
        """Загрузка файла на сервер"""
        try:
            self.logger.info(f"Начало загрузки файла {file_path}")
            with open(file_path, 'rb') as f:
                files = {field_name: f}
                data = extra_data or {}
                response = self._make_request('POST', endpoint, files=files, data=data, headers=headers)
                self.logger.info(f"Файл {file_path} успешно загружен")
                return self._handle_response(response)
        except IOError as e:
            error_msg = f"Ошибка чтения файла {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise ApiError(error_msg)
