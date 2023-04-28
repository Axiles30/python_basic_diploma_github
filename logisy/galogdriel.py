from loguru import logger

logger.add("debug.json", format="{time} {level} {message}",
           level="DEBUG", rotation="10 KB", compression="zip",
           serialize=True)

# for _ in range(1000):
# 	logger.debug("Hello, World (debug)!")




# Настраиваем логирование
logger.add("debug.log", rotation="500 MB", compression="zip", enqueue=True)

# Пример использования логирования
try:
    # some code here
except Exception as e:
    logger.exception(e)