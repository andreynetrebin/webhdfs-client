# WebHDFS Клиент
<img width="680" height="618" alt="hdfs_api" src="https://github.com/user-attachments/assets/36d82bf6-f8ee-4942-a191-f3ce25a46f5e" />

Клиент WebHDFS для Python, который использует пользовательский инструмент API.

## Возможности
- Поддержка всех основных операций с HDFS: создание директорий, загрузка и чтение файлов, удаление и переименование.
- Получение метаданных файлов и директорий.
- Поддержка аутентификации с использованием токенов.
- Логирование запросов и ответов для удобства отладки.
- Обработка ошибок с подробными сообщениями.

## Установка

Вы можете установить пакет, используя pip:

```bash
pip install -e .
```
Это установит WebHDFS клиент и все его зависимости, включая RestApiTool, который будет загружен либо локально, либо из вашего онлайн-репозитория.

## Использование

```python
from webhdfs_client import WebHDFSClient

client = WebHDFSClient('http://namenode:50070/webhdfs/v1', username='hdfs')

# Создание директории
client.mkdirs('/test_dir')

# Получение списка файлов
status = client.list_status('/')
print(status)

# Удаление директории
client.delete_file('/test_dir', recursive=True)
```

## Запуск тестов
```bash
python -m unittest discover -s tests
```

## Лицензия
Этот проект лицензирован под лицензией MIT.
