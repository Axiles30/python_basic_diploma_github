from loguru import logger

logger.add("debug.json", format="{time} {level} {message}",
           level="DEBUG", rotation="10 KB", compression="zip",
           serialize=True)

# for _ in range(1000):
# 	logger.debug("Hello, World (debug)!")