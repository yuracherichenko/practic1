import json
import random
from datetime import datetime
import time
import sched
import os
import logging

# Конфигурация
DOWNLOAD_DIR = "json/download/"
LOG_DIR = "json/log/"
GENERATION_LOG = f'{LOG_DIR}serialize-{datetime.now().strftime("%Y%m%d")}.log'
GENERATION_INTERVAL = 10  # Интервал между генерацией JSON
MAX_GENERATIONS = 5       # Количество генераций JSON

# Убедимся, что директории существуют
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    filename=GENERATION_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("generation")


class Article:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
        self.likes = random.randint(10, 100)

    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "datetime": self.datetime,
            "likes": self.likes,
            "className": self.__class__.__name__
        }


def generate_json_data(iteration):
    try:
        title = f'Заголовок - {random.randint(1, 9999)}'
        body = f'Некоторый текст - {random.randint(1000, 9999999)}'
        article = Article(title, body)

        file_name = f"{iteration}-{datetime.now().strftime('%Y%m%d%H%M%S')}-data.json"
        file_path = os.path.join(DOWNLOAD_DIR, file_name)

        with open(file_path, "w") as file:
            json.dump(article.to_dict(), file, ensure_ascii=False, indent=4)

        logger.info(f"Файл создан: {file_name}")
    except Exception as e:
        logger.error(f"Ошибка при создании JSON: {e}")


def schedule_generation(sc, iteration):
    if iteration <= MAX_GENERATIONS:
        generate_json_data(iteration)
        sc.enter(GENERATION_INTERVAL, 1, schedule_generation, (sc, iteration + 1))


def main():
    logger.info("Запуск генерации JSON-файлов")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(1, 1, schedule_generation, (scheduler, 1))
    scheduler.run()
    logger.info("Завершение генерации")


if __name__ == "__main__":
    main()
