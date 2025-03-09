import os
import glob
import asyncio
import time
from pyrogram import Client, filters

last_cleanup_time = 0

async def delete_temp_files():
    global last_cleanup_time
    while True:
        await asyncio.sleep(100)  # انتظار 100 ثانية بين كل عملية تنظيف
        current_time = time.time()
        
        if current_time - last_cleanup_time >= 100:
            # حذف الملفات من مجلد محدد بدلاً من `/`
            cache_dir = os.path.join(os.getcwd(), "cache")  # ضع الملفات المؤقتة في مجلد cache
            downloads_dir = os.path.join(os.getcwd(), "downloads")  # تأكد أن المجلد موجود
           
            for directory in [cache_dir, downloads_dir]:
                if os.path.exists(directory):
                    for file in os.listdir(directory):
                        file_path = os.path.join(directory, file)
                        if os.path.isfile(file_path):  # حذف فقط الملفات وليس المجلدات
                            os.remove(file_path)

            # حذف الملفات بتنسيقات محددة
            files_to_delete = glob.glob("*.webm") + glob.glob("*.jpg") + glob.glob("*.png")
            for file_path in files_to_delete:
                if os.path.isfile(file_path):
                    os.remove(file_path)

            last_cleanup_time = current_time
            print("✅ تم حذف الملفات المؤقتة بنجاح  بابا . @Fox4566")

asyncio.ensure_future(delete_temp_files())
