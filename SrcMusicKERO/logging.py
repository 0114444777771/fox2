import logging
import sys

# تهيئة نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),  # عرض السجلات في وحدة التحكم
        logging.FileHandler("bot.log", encoding="utf-8", mode="a"),  # حفظ السجلات في ملف
    ],
)

# إنشاء كائن السجل الرئيسي
LOGGER = logging.getLogger("BotLogger")

# التحقق من عمل السجلات
LOGGER.info("Logger has been initialized successfully!")
