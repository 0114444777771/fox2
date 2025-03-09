import socket
import time
import heroku3
from pyrogram import filters
import config
from SrcMusicKERO.core.mongo import mongodb
from .logging import LOGGER  # تأكد من أن LOGGER معرف بشكل صحيح

SUDOERS = filters.user()
HAPP = None
_boot_ = time.time()

# التحقق مما إذا كان يعمل على Heroku
def is_heroku():
    return "heroku" in socket.getfqdn()

# دالة تحديث قاعدة البيانات
def dbb():
    global db
    db = {}
    LOGGER("ميوزك فوكس").info("تم تحديث قاعدة بيانات البوت ...✓")

# دالة تحميل قائمة المطورين
async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER("ميوزك فوكس").info("تم تحميل قائمة مطورين البوت ...✓")

# دالة الاتصال بـ Heroku وإضافة المتغيرات
def heroku():
    global HAPP
    if is_heroku():  # تم تعديل الخطأ هنا بإضافة الأقواس
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                heroku_conn = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = heroku_conn.app(config.HEROKU_APP_NAME)
                heroku_var = HAPP.config()

                # التأكد من أن الفارات غير موجودة قبل إضافتها
                if "API_ID" not in heroku_var:
                    heroku_var["API_ID"] = "22624445"
                    heroku_var["API_HASH"] = "53bc68926ff18228dbbd89794211300b"
                    heroku_var["MONGO_DB_URI"] = "mongodb+srv://foxnasa603:admiNn12f@cluster0.6bcyg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                    LOGGER("ميوزك فوكس").info("تم إضافة متغيرات البيئة بنجاح ✓")
                else:
                    LOGGER("ميوزك فوكس").info("متغيرات البيئة موجودة مسبقًا ✓")

            except Exception as e:
                LOGGER(__name__).warning(
                    f"⚠️ يرجى التأكد من إضافة مفتاح هيروكو واسم التطبيق بشكل صحيح.\nالخطأ: {e}"
                )
