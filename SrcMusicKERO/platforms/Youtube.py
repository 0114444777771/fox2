import asyncio
import re
from typing import Union

import yt_dlp
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch


async def shell_cmd(cmd):
    """ تشغيل أوامر النظام داخل asyncio """
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    return out.decode("utf-8") if not errorz else errorz.decode("utf-8")


# 🔹 تعديل مسار ملف الكوكيز بدون "root"
cookies_file = "/fox2/cookies/cookies_fixed.txt"

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.listbase = "https://youtube.com/playlist?list="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message: Message):
        """ استخراج رابط الفيديو من الرسالة """
        text = message.text or message.caption  
        if not text:
            print("❌ لا يوجد نص في الرسالة!")
            return None

        video_id_match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|watch\?v=)([\w-]+)", text)
        if video_id_match:
            url = self.base + video_id_match.group(1)
            print(f"✅ رابط الفيديو المستخرج: {url}")
            return url
        else:
            print("❌ لم يتم العثور على رابط فيديو!")
            return None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        """ جلب رابط تشغيل الفيديو باستخدام yt-dlp """
        if videoid:
            link = self.base + link
        print(f"🔹 تشغيل video() مع الرابط: {link}")

        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookies_file,
            "-g",
            "-f", "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        # طباعة المخرجات للتصحيح
        print(f"🔹 yt-dlp stdout: {stdout.decode().strip()}")
        print(f"🔹 yt-dlp stderr: {stderr.decode().strip()}")

        if stdout:
            return 1, stdout.decode().strip()
        else:
            return 0, stderr.decode().strip()


async def process_message(message: Message):
    """ تشغيل الأغنية عند استلام رابط يوتيوب في رسالة """
    youtube = YouTubeAPI()
    url = await youtube.url(message)

    if not url:
        print("❌ لم يتم العثور على رابط فيديو في الرسالة!")
        return "❌ لم يتم العثور على رابط فيديو!"

    status, video_url = await youtube.video(url)

    if status == 1:
        print(f"🎵 رابط التشغيل: {video_url}")
        return video_url
    else:
        print(f"❌ خطأ في جلب الفيديو: {video_url}")
        return f"❌ خطأ في جلب الفيديو: {video_url}"


# ✅ **مثال تشغيل الفيديو**
async def main():
    class FakeMessage:
        text = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        caption = None

    message = FakeMessage()
    result = await process_message(message)
    print("🔹 النتيجة:", result)

if __name__ == "__main__":
    asyncio.run(main())
