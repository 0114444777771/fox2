import asyncio
import glob
import os
import random
from typing import Union
import yt_dlp
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from config import PLAYLIST_IMG_URL, sudoers as SUDOERS, adminlist  # ✅ تم تصحيح الخطأ هنا

cookies_file = "/fox2/cookies/cookies_fixed.txt"

# دمج الكودين هنا
async def shell_cmd(cmd):
    """ تشغيل أوامر النظام داخل asyncio """
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    return out.decode("utf-8") if not errorz else errorz.decode("utf-8")

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
            return None

        video_id_match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|watch\?v=)([\w-]+)", text)
        if video_id_match:
            return self.base + video_id_match.group(1)
        return None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        """ جلب رابط الفيديو باستخدام yt-dlp """
        if videoid:
            link = self.base + link
        print(f"🔹 تشغيل video() مع الرابط: {link}")
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookies_file,
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return (1, stdout.decode().split("\n")[0]) if stdout else (0, stderr.decode())

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        """ جلب قائمة تشغيل من YouTube """
        if videoid:
            link = self.listbase + link
        print(f"🔹 تشغيل playlist() مع الرابط: {link}")
        playlist = await shell_cmd(
            f"yt-dlp --cookies {cookies_file} -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        return [key for key in playlist.split("\n") if key]

    async def download(self, client, bot_username, link, video: Union[bool, str] = None):
        loop = asyncio.get_running_loop()
        logger = await get_logger(bot_username)
        output_file = f"{bot_username}_{random.randint(1000, 9999)}.%(ext)s"

        ydl_opts = {
            "format": "bestvideo+bestaudio/best" if video else "bestaudio/best",
            "outtmpl": output_file,
            "quiet": True,
            "nocheckcertificate": True,
            "cookiefile": cookies_file,
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if not video else []
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await loop.run_in_executor(None, lambda: ydl.download([f"https://youtube.com{link}"]))
        except Exception as e:
            error_message = f"حدث خطأ أثناء التحميل: {e}"
            print(error_message)
            await client.send_message(logger, f"**فشل التحميل:**\n`{error_message}`")
            return None

        files = glob.glob(f"{bot_username}_*.mp3" if not video else f"{bot_username}_*.*")
        if not files:
            await client.send_message(logger, "**فشل تحميل الملف من يوتيوب. قد يكون الفيديو خاص أو به قيود.**")
            return None

        file_path = files[0]
        sent_msg = await client.send_audio(logger, file_path) if not video else await client.send_video(logger, file_path)
        downloaded_path = await sent_msg.download()

        try:
            os.remove(file_path)
        except Exception as e:
            print(f"خطأ أثناء حذف الملف: {e}")

        return downloaded_path

# **مثال استدعاء `url()` و `video()` معًا**
async def process_message(client, message: Message):
    youtube = YouTubeAPI()
    url = await youtube.url(message)
    
    if url:
        print(f"✅ رابط الفيديو المستخرج: {url}")
        status, video_url = await youtube.video(url)
        
        if status == 1:
            print(f"🎵 رابط التشغيل: {video_url}")
            # استدعاء دالة التنزيل هنا
            downloaded_path = await youtube.download(client, "bot_username", url, video=True)
            if downloaded_path:
                print(f"📥 تم تنزيل الفيديو إلى: {downloaded_path}")
        else:
            print(f"❌ خطأ في جلب الفيديو: {video_url}")
    else:
        print("❌ لم يتم العثور على رابط فيديو في الرسالة!")
