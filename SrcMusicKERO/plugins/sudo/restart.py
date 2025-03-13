import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from SrcMusicKERO.plugins.play.filters import command
from pyrogram import filters

import config
from SrcMusicKERO import app
from SrcMusicKERO.misc import HAPP, SUDOERS
from SrcMusicKERO.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from SrcMusicKERO.utils.decorators.language import language
from SrcMusicKERO.utils.pastebin import ZelzalyBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def is_heroku():
    return "heroku" in socket.getfqdn()

@app.on_message(command(["getlog", "logs", "السجلات"]) & SUDOERS)
@language
async def log_(client, message, _):
    try:
        await message.reply_document(document="log.txt")
    except:
        await message.reply_text(_["server_1"])

@app.on_message(command(["تحديث", "حدث"]) & SUDOERS)
@language
async def update_(client, message, _):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["server_2"])
    response = await message.reply_text(_["server_3"])
    
    try:
        repo = Repo()
    except (GitCommandError, InvalidGitRepositoryError):
        return await response.edit(_["server_4"])

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)
    
    updates = ""
    repo_url = repo.remotes.origin.url.split(".git")[0]
    for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        updates += f"<b>➣ {info.summary}</b> - {info.author}\n"

    if not updates:
        return await response.edit(_["server_6"])

    update_text = f"<b>➣ يوجد تحديث جديد للبوت</b>\n\n<b>➣ التحديثات :</b>\n{updates}"
    if len(update_text) > 4096:
        url = await ZelzalyBin(updates)
        update_text = f"<b>➣ يوجد تحديث جديد للبوت</b>\n\n<a href={url}>اضغط هنا لرؤية التحديثات</a>"

    await response.edit(update_text, disable_web_page_preview=True)
    os.system("git stash && git pull")

    served_chats = await get_active_chats()
    for x in served_chats:
        try:
            await app.send_message(chat_id=int(x), text=_["server_8"].format(app.mention))
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    if await is_heroku():
        try:
            os.system("git push heroku master")
            return
        except Exception as err:
            await response.edit(f"{update_text}\n\n{_['server_9']}")
            return await app.send_message(chat_id=config.LOGGER_ID, text=_["server_10"].format(err))
    else:
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && exec bash start.sh")

@app.on_message(command(["اعاده تشغيل"]) & SUDOERS)
async def restart_(_, message):
    response = await message.reply_text("- جـارِ إعـادة التشغيـل ...")
    
    active_chats = await get_active_chats()
    for x in active_chats:
        try:
            await app.send_message(chat_id=int(x), text=f"» {app.mention} في وضع إعادة التشغيل...")
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    try:
        shutil.rmtree("downloads", ignore_errors=True)
        shutil.rmtree("raw_files", ignore_errors=True)
        shutil.rmtree("cache", ignore_errors=True)
    except:
        pass
    
    await response.edit_text("» جـارِ اعـادة تشغيـل البـوت ...\n» انتظـر ⏳...")
    os.system(f"kill -9 {os.getpid()} && exec bash start.sh")
