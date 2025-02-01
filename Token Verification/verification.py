import string, random, os, sys
from urllib.parse import quote
from time import time
from urllib3 import disable_warnings
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

from cloudscraper import create_scraper
from motor.motor_asyncio inport AsyncIOMotorClient


# Config Variables 😄
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')   # YOUR BOT TOKEN FROM @Botfather
VERIFY_PHOTO = os.environ.get('VERIFY_PHOTO', '')  # YOUR VERIFY PHOTO LINK
SHORTLINK_URL = os.environ.get('SHORTLINK_URL', '') # YOUR SHORTLINK URL LIKE:- site.com
SHORTLINK_API = os.environ.get('SHORTLINK_API', '') # YOUR SHORTLINK API LIKE:- ma82owowjd9hw6_js7
VERIFY_EXPIRE = os.environ.get('VERIFY_EXPIRE', '') # VERIFY EXPIRE TIME IN SECONDS. LIKE:- 0 (ZERO) TO OFF VERIFICATION 
VERIFY_TUTORIAL = os.environ.get('VERIFY_TUTORIAL', '') # LINK OF TUTORIAL TO VERIFY 
DATABASE_URI = os.environ.get('DATABASE_URI', '') # MONGODB DATABASE URL


bot_id = BOT_TOKEN.split(':')[0]
verify_dict = {}
missing=[v for v in ["BOT_TOKEN", "VERIFY_PHOTO", "SHORTLINK_URL", "SHORTLINK_API", "VERIFY_EXPIRE", "VERIFY_TUTORIAL"] if not os.getenv(v)]; sys.exit(f"Missing: {', '.join(missing)}") if missing else None

# Databse Code
class VerifyDB():
    def __init__(self):
        self._dbclient = AsyncIOMotorClient(DATABASE_URI)
        self._db = self._dbclient['verify-db']
        self._verifydb = self._db[bot_id]  

    async def get_verify_status(self, user_id):
        if status := await self._verifydb.find_one({'id': user_id}):
            return status.get('verify_status', 0)
        return 0

    async def update_verify_status(self, user_id):
        await self._verifydb.update_one({'id': user_id}, {'$set': {'verify_status': time()}}, upsert=True)

verifydb = VerifyDB()

# Helper Functions
async def is_user_verified(user_id):
    if not VERIFY_EXPIRE:
        return True
    isveri = await verifydb.get_verify_status(user_id)
    if not isveri or (time() - isveri) >= float(Config.VERIFY_EXPIRE):
        return False
    return True    
    
async def send_verification(client, message, text=None):
    username = await client.get_me().username
    verify_token = await get_verify_token(client, message.from_user.id, f"https://telegram.me/{username}?start=")
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('Get Token', url=verify_token)],
        [InlineKeyboardButton('🎬 Tutorial 🎬', url=VERIFY_TUTORIAL)],
    ]),
    if not text:
        text = f"""<b>Hi 👋 {message.from_user.mention}, 
Your Ads Token Has Been Expired, Kindly Get A New Token To Continue Using This Bot.
         ㅤㅤㅤㅤㅤ   - Thank You 
\nआपका विज्ञापन टोकन समाप्त हो गया है, बॉट को फिर से उपयोग करने के लिए नया टोकन लें!
         ㅤㅤㅤㅤㅤㅤㅤ- धन्यवाद
\nToken Validity: {get_readable_time(VERIFY_EXPIRE)}
\n#Verification...⌛</b>"""
    
    await message.reply_photo(
        photo=VERIFY_PHOTO,
        caption=text,
        reply_markup=buttons,
        reply_to_message_id=message.id,
        protect_content=True,
    )
 
async def get_verify_token(bot, userid, link):
    vdict = verify_dict.setdefault(userid, {})
    short_url = vdict.get('short_url')
    if not short_url:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        long_link = f"{link}verify-{userid}-{token}"
        short_url = await short_url(long_link)
        vdict.update({'token': token, 'short_url': short_url})
    return short_url

async def short_url(longurl, _shortener = SHORTLINK_URL, _shortener_api = SHORTLINK_API):
    cget = create_scraper().request
    disable_warnings()
    try:
        url = f'https://{_shortener}/api'
        params = {'api': _shortener_api,
                  'url': longurl,
                  'format': 'text',
                 }
        res = cget('GET', url, params=params)
        if res.status_code == 200 and res.text:
            return res.text
        else:
            params['format'] = 'json'
            res = cget('GET', url, params=params)
            res = res.json()
            if res.status_code == 200:
                return res.get('shortenedUrl', long_url)
    except Exception as e:
        return long_link

async def validate_token(client, message, data):
    user_id = message.from_user.id
    vdict = verify_dict.setdefault(user_id, {})
    dict_token = vdict.get('token', None)
    if not dict_token:
        return await send_verification(client, message, text="<b>Tʜᴀᴛ's Nᴏᴛ Yᴏᴜʀ Vᴇʀɪғʏ Tᴏᴋᴇɴ 🥲...\n\n\nTᴀᴘ Oɴ Vᴇʀɪғʏ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Yᴏᴜʀs</b>")  
    _, uid, token = data.split("-")
    if uid != str(user_id):
        return await send_verification(client, message, text="<b>Tʜᴀᴛ's Nᴏᴛ Yᴏᴜʀ Vᴇʀɪғʏ Tᴏᴋᴇɴ 🥲...\n\n\nTᴀᴘ Oɴ Vᴇʀɪғʏ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Yᴏᴜʀs</b>")
    elif dict_token != token:
        return await send_verification(client, message, text="<b>Iɴᴠᴀʟɪᴅ Oʀ Exᴘɪʀᴇᴅ Tᴏᴋᴇɴ 🔗...</b>")
    await message.reply_photo(photo=VERIFY_PHOTO,
                              caption=f'<b>Wᴇʟᴄᴏᴍᴇ Bᴀᴄᴋ 😁, Nᴏᴡ Yᴏᴜ Cᴀɴ Usᴇ Mᴇ Fᴏʀ {get_readable_time(VERIFY_EXPIRE)}.\n\n\nEɴᴊᴏʏʏʏ...❤️</b>',
                              reply_to_message_id=message.id,
                             )
    vdict = {}
    
def get_readable_time(seconds):
    periods = [('ᴅ', 86400), ('ʜ', 3600), ('ᴍ', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result


# Usage 😀

                
