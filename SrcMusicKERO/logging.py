import logging
import sys

# تحقق من sys.stdout لتجنب NoneType
stream_handler = logging.StreamHandler(sys.stdout if sys.stdout else sys.__stdout__)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        stream_handler,
        logging.FileHandler("bot.log", encoding="utf-8", mode="w"),  # حفظ السجلات في ملف
    ],
)

def LOGGER(name: str) -> logging.Logger:
    """وظيفة تُعيد كائن Logger بإعدادات محسنة."""
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout if sys.stdout else sys.__stdout__)
        handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger
