import base64
import hmac
import struct
import time
from hashlib import sha1
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode

import config

bot = Bot(token=config.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == 427176025:
        await message.answer(f"<code>{get_guard_code(config.shared_secret)}</code>")
    else:
        await message.answer(f"<b>You are not admin!</b>")


def get_guard_code(shared_secret: str) -> str:
    timestamp = int(time.time())
    time_buffer = struct.pack('>Q', timestamp // 30)
    time_hmac = hmac.new(base64.b64decode(shared_secret), time_buffer, digestmod=sha1).digest()
    begin = ord(time_hmac[19:20]) & 0xf
    full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] & 0x7fffffff
    chars = '23456789BCDFGHJKMNPQRTVWXY'
    code = ''
    for _ in range(5):
        full_code, i = divmod(full_code, len(chars))
        code += chars[i]
    return code


if __name__ == '__main__':
    executor.start_polling(dp)
