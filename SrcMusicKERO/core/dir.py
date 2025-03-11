import os
from ..logging import LOGGER

def dirr():
    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg", ".png")):
            os.remove(file)

    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    if "cache" not in os.listdir():
        os.mkdir("cache")

    LOGGER.info("تم تحـديث السـورس ...✓")
