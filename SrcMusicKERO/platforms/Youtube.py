import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from SrcMusicKERO.utils.database import is_on_off
from SrcMusicKERO.utils.formatters import time_to_seconds

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

    async def download(self, link: str, title: str, format_id: str, songvideo: bool = False, songaudio: bool = False):
        """ تحميل الصوت أو الفيديو من YouTube """
        loop = asyncio.get_running_loop()

        def download_audio():
            ydl_opts = {
                "format": format_id,
                "outtmpl": f"downloads/{title}.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookies_file,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

        def download_video():
            ydl_opts = {
                "format": f"{format_id}+140",
                "outtmpl": f"downloads/{title}",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookies_file,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

        if songvideo:
            print(f"🔹 تحميل فيديو: {title}")
            await loop.run_in_executor(None, download_video)
            return f"downloads/{title}.mp4"
        elif songaudio:
            print(f"🔹 تحميل صوت: {title}")
            await loop.run_in_executor(None, download_audio)
            return f"downloads/{title}.mp3"
