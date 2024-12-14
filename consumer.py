import json
import shutil
import os
import logging
from datetime import datetime

# Конфигурация
DOWNLOAD_DIR = "json/download/"
LOADED_DIR = "json/loaded/"
ERROR_DIR = "json/error/"
LOG_DIR = "json/log/"
PROCESSING_LOG = f'{LOG_DIR}deserialize-{datetime.now().strftime("%Y%m%d")}.log'
PROCESSING_INTERVAL = 10  # Интервал между обработкой JSON
MAX_PROCESSING = 20       # Количество обработок JSON

# Убедимся, что директории существуют
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOADED_DIR, exist_ok=True)
os.makedirs(ERROR_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    filename=PROCESSING_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("processing")


class Article:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
        self.likes = random.randint(10, 100)

    @staticmethod
    def from_dict(data):
        article = Article(data["title"], data["body"])
        article.datetime = data.get("datetime", article.datetime)
        article.likes = data.get("likes", article.likes)
        return article

    def __str__(self):
        return f"Title: {self.title}\nBody: {self.body}\nDate: {self.datetime}\nLikes: {self.likes}"


def process_json_files():
    for filename in os.listdir(DOWNLOAD_DIR):
        if filename.endswith(".json"):
            full_path = os.path.join(DOWNLOAD_DIR, filename)
            try:
                with open(full_path, "r") as file:
                    data = json.load(file)

                article = Article.from_dict(data)
                logger.info(f"Обработан файл: {filename}")
                print(article)
                shutil.move(full_path, os.path.join(LOADED_DIR, filename))

            except Exception as e:
                logger.error(f"Ошибка при обработке файла {filename}: {e}")
                shutil.move(full_path, os.path.join(ERROR_DIR, filename))


def main():
    logger.info("Запуск обработки JSON-файлов")
    for _ in range(MAX_PROCESSING):
        process_json_files()
        logger.info("Обработка завершена. Ожидание следующего цикла...")
        time.sleep(PROCESSING_INTERVAL)
    logger.info("Завершение обработки")


if __name__ == "__main__":
    main()
