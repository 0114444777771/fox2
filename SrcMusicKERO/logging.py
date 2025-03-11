import logging
import sys

# إنشاء معالج تسجيل لطباعة السجلات إلى وحدة التحكم (stdout)
stream_handler = logging.StreamHandler(sys.stdout if sys.stdout else sys.__stdout__)

# تهيئة نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        stream_handler,  # عرض السجلات في وحدة التحكم
        logging.FileHandler("bot.log", encoding="utf-8", mode="a"),  # حفظ السجلات في ملف
    ],
)

def LOGGER(name: str) -> logging.Logger:
    """إرجاع كائن Logger بإعدادات محسنة."""
    logger = logging.getLogger(name)

    # التأكد من عدم إضافة معالجات متعددة
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout if sys.stdout else sys.__stdout__)
        handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger

# إنشاء كائن السجل الرئيسي للبوت
log = LOGGER("BotLogger")

# التحقق من عمل السجلات
log.info("Logger has been initialized successfully!")
