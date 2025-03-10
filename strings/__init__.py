from pyrogram.types import InlineKeyboardButton
from SrcMusicKERO import app

# تخزين لغة كل مستخدم
user_languages = {}

def get_text(user_id, key):
    """ استرجاع النص المناسب حسب لغة المستخدم """
    from strings import get_string  # استيراد داخل الدالة لتجنب المشكلة
    lang = user_languages.get(user_id, "ar")  # العربية هي الافتراضية
    return get_string(lang).get(key, key)  # جلب النص من ملف الترجمة

def start_panel(user_id):
    """ إنشاء لوحة الأزرار عند بدء التشغيل """
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(user_id, "add_group"), 
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "choose_language"), 
                callback_data="change_lang"
            ),
        ]
    ]
    return buttons

def private_panel(user_id):
    """ إنشاء لوحة الأزرار للمحادثات الخاصة """
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(user_id, "add_group"), 
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "developer"), 
                url="https://t.me/Fox4566"
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "source_channel"), 
                url="https://t.me/PX_CBL"
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "choose_language"), 
                callback_data="change_lang"
            ),
        ]
    ]
    return buttons
