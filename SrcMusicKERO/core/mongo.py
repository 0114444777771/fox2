from motor.motor_asyncio import AsyncIOMotorClient
import traceback
from config import MONGO_DB_URI
from ..logging import LOGGER

LOGGER.info("ميوزك فوكس - جـارِ الاتصـال بقاعـدة البيانـات . . .")

try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_["fox_database"]  # غيّر "fox_database" إلى اسم القاعدة الفعلي
    LOGGER.info("تم الاتصـال بقاعـدة البيانـات ...✓")
except Exception as e:
    LOGGER.error(f"حدث خطأ أثناء الاتصال بقاعدة البيانات:\n{traceback.format_exc()}")
    exit()
