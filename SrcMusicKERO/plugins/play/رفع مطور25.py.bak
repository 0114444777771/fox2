import json
from pyrogram import Client, filters
from AarohiX import app

def load_tom_devs():
    try:
        with open('tom_devs.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'devs': {}}

def dump_tom_devs(data):
    with open('tom_devs.json', 'w') as file:
        json.dump(data, file, indent=4)

def is_tom(client, message):
    # تحقق من أن المستخدم هو المطور الثانوي
    return message.from_user.id == TOM_ID

def is_basic_dev(client, message):
    # تحقق من أن المستخدم هو المطور الأساسي
    return message.from_user.id == BASIC_DEV_ID

def is_owner_id(client, message):
    # تحقق من أن المستخدم هو المالك
    return message.from_user.id == OWNER_ID

def is_dev(client, message):
    # تحقق من أن المستخدم هو مطور معتمد
    user_id = str(message.from_user.id)
    tom_devs = load_tom_devs()
    return user_id in tom_devs['devs']

@app.on_message(filters.command("رفع مطور", ""))
def promote_devs(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
    elif message.reply_to_message is None:
        target = message.text.split()[2]
        user = app.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = app.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            message.reply_text("لا يمكن العثور على المستخدم")
            return

    tom_devs = load_tom_devs()

    if not (is_tom(client, message) or is_basic_dev(client, message) or is_owner_id(client, message)):
        message.reply_text("""◍ انت لست المطور الثانوي
√""")
        return

    if user_id in tom_devs['devs']:
        message.reply_text("""◍ هذا المستخدم مطور بالفعل
√""")
    else:
        tom_devs['devs'][user_id] = True
        dump_tom_devs(tom_devs)
        message.reply_text("""◍ تم رفع المستخدم ليصبح مطور
√""")

@app.on_message(filters.command("المطورين", ""))
def get_devs(client, message):
    chat_id = str(message.chat.id)
    tom_devs = load_tom_devs()
    if not (is_tom(client, message) or is_basic_dev(client, message) or is_owner_id(client, message) or is_dev(client, message)):
        message.reply_text("""◍ انت لست المطور
√""")
        return

    if 'devs' not in tom_devs or not tom_devs['devs']:
        message.reply_text("لا يوجد مطورين حتى الأن")
        return

    admins = tom_devs['devs']
    admin_names = []
    for admin_id in admins:
        user = app.get_users(int(admin_id))
        if user:
            admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")

    if admin_names:
        admin_list = "\n".join(admin_names)
        message.reply_text(f"◍ قائمة المطورين:\n\n{admin_list}")
    else:
        message.reply_text("تعذر العثور على معلومات المطورين")

@app.on_message(filters.command("تنزيل مطور", ""))
def demote_devs(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
    elif message.reply_to_message is None:
        target = message.text.split()[2]
        user = app.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = app.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            message.reply_text("لا يمكن العثور على المستخدم")
            return
    chat_id = str(message.chat.id)

    tom_devs = load_tom_devs()
    if not (is_tom(client, message) or is_basic_dev(client, message) or is_owner_id(client, message)):
        message.reply_text("""◍ انت لست المطور الثانوي
√""")
        return

    if user_id not in tom_devs['devs']:
        message.reply_text("""◍ هذا المستخدم ليس مطور لتنزيله
√""")
    else:
        del tom_devs['devs'][user_id]
        dump_tom_devs(tom_devs)
        message.reply_text("""◍ تم تنزيل المستخدم من المطورين بنجاح
√""")

@app.on_message(filters.command("مسح المطورين", ""))
def clear_devs(client, message):
    chat_id = str(message.chat.id)
    tom_devs = load_tom_devs()
    if not (is_tom(client, message) or is_basic_dev(client, message) or is_owner_id(client, message)):
        message.reply_text("""◍ انت لست المطور الثانوي
√""")
        return

    if 'devs' in tom_devs:
        tom_devs['devs'] = {}
        dump_tom_devs(tom_devs)
        message.reply_text("""◍ تم مسح المطورين بنجاح
√""")
    else:
        message.reply_text("لا يوجد مطورين ليتم مسحهم")

