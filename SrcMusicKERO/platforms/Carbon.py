import random
from os.path import realpath
import aiohttp
import aiofiles  # إضافة المكتبة لاستخدام الكتابة غير المتزامنة
from aiohttp import client_exceptions


class UnableToFetchCarbon(Exception):
    pass


themes = [
    "3024-night", "a11y-dark", "blackboard", "base16-dark", "base16-light",
    "cobalt", "duotone-dark", "dracula-pro", "hopscotch", "lucario",
    "material", "monokai", "nightowl", "nord", "oceanic-next",
    "one-light", "one-dark", "panda-syntax", "parasio-dark", "seti",
    "shades-of-purple", "solarized+dark", "solarized+light", "synthwave-84",
    "twilight", "verminal", "vscode", "yeti", "zenburn",
]

colour = [
    "#FF0000", "#FF5733", "#FFFF00", "#008000", "#0000FF", "#800080", 
    "#A52A2A", "#FF00FF", "#D2B48C", "#00FFFF", "#808000", "#800000", 
    "#00FFFF", "#30D5C8", "#00FF00", "#008080", "#4B0082", "#EE82EE", 
    "#FFC0CB", "#000000", "#FFFFFF", "#808080",
]


class CarbonAPI:
    def __init__(self):
        self.language = "auto"
        self.drop_shadow = True
        self.drop_shadow_blur = "68px"
        self.drop_shadow_offset = "20px"
        self.font_family = "JetBrains Mono"
        self.width_adjustment = True
        self.watermark = False

    async def generate(self, text: str, user_id):
        async with aiohttp.ClientSession(
            headers={"Content-Type": "application/json"},
        ) as ses:
            params = {
                "code": text,
                "backgroundColor": random.choice(colour),
                "theme": random.choice(themes),
                "dropShadow": self.drop_shadow,
                "dropShadowOffsetY": self.drop_shadow_offset,
                "dropShadowBlurRadius": self.drop_shadow_blur,
                "fontFamily": self.font_family,
                "language": self.language,
                "watermark": self.watermark,
                "widthAdjustment": self.width_adjustment,
            }
            try:
                request = await ses.post(
                    "https://carbonara.solopov.dev/api/cook",
                    json=params,
                )
                request.raise_for_status()  # تأكد من نجاح الطلب
            except client_exceptions.ClientConnectorError:
                raise UnableToFetchCarbon("Can not reach the Host!")

            resp = await request.read()
            file_path = f"cache/carbon{user_id}.jpg"
            
            # استخدام aiofiles للكتابة غير المتزامنة
            async with aiofiles.open(file_path, "wb") as f:
                print(f"f type: {type(f)}")  # إضافة طباعة لفحص النوع
                await f.write(resp)

            return realpath(file_path)
