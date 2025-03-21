from SrcMusicKERO.core.bot import Zelzaly
from SrcMusicKERO.core.dir import dirr
from SrcMusicKERO.core.userbot import Userbot
from SrcMusicKERO.misc import dbb, heroku

from .logging import LOGGER

dirr()
dbb()
heroku()

app = Zelzaly()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()