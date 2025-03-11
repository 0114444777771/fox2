import logging
import sys

# تهيئة السجلات بمستوى INFO لإخفاء DEBUG
logging.basicConfig(
    level=logging.INFO,  # تغيير إلى INFO لإخفاء DEBUG
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),  # طباعة السجلات إلى الشاشة
        logging.FileHandler("bot.log", encoding="utf-8", mode="w"),  # حفظ السجلات في ملف
    ],
)

# تقليل مستوى السجل لبعض المكتبات لتجنب الضوضاء
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)  # تغيير إلى WARNING
logging.getLogger("pytgcalls").setLevel(logging.WARNING)  # تغيير إلى WARNING


def LOGGER(name: str) -> logging.Logger:
    """وظيفة تُعيد كائن Logger بإعدادات محسنة."""
    logger = logging.getLogger(name)

    if not logger.hasHandlers():  # التأكد من عدم تكرار الـ Handlers
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)  # التأكد من عدم تسجيل DEBUG
    return logger
