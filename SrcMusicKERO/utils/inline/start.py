from pyrogram.types import InlineKeyboardButton

import config
from SrcMusicKERO import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ أضفني إلى مجموعتك", 
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ أضفني إلى مجموعتك", 
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(text="👨‍💻 المطوّر", url="https://t.me/Fox4566"),
        ],
        [
            InlineKeyboardButton(text="📡 قناة السورس", url="https://t.me/PX_CBL"),
        ],
    ]
    return buttons
