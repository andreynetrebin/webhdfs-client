# WebHDFS Клиент

Клиент WebHDFS для Python, который использует пользовательский инструмент API.

## Возможности
- Поддержка всех основных операций с HDFS: создание директорий, загрузка и чтение файлов, удаление и переименование.
- Получение метаданных файлов и директорий.
- Поддержка аутентификации с использованием токенов.
- Логирование запросов и ответов для удобства отладки.
- Обработка ошибок с подробными сообщениями.

## Установка

Вы можете установить пакет, используя pip. Если вы хотите использовать `RestApiTool` из онлайн-репозитория, выполните следующие команды:

```bash
pip install git+https://github.com/andreynetrebin/api-tool.git
pip install -e .
```
Если вы хотите установить только WebHDFS клиент, используйте:

```bash
pip install -e .
```

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
