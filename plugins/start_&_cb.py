from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep
import asyncio   # <-- REQUIRED for the animation


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, Bro You are banned.")
        return

    # Animation sequence
    m = await message.reply_text("ʜᴇʜᴇ..ɪ'ᴍ Govar!\nᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ. . .")
    await asyncio.sleep(0.4)
    await m.edit_text("🎊")
    await asyncio.sleep(0.5)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("Mg Mg!...")
    await asyncio.sleep(0.4)
    await m.delete()

    # Send sticker after animation
    await message.reply_sticker(
        "CAACAgUAAxkBAAECroBmQKMAAQ-Gw4nibWoj_pJou2vP1a4AAlQIAAIzDxlVkNBkTEb1Lc4eBA"
    )

    # Inline buttons
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('⛅ ᴜᴘᴅᴀᴛᴇs', url='https://t.me/All_animes_in_teluguu_vs'),
            InlineKeyboardButton('🌨️ sᴜᴘᴘᴏʀᴛ', url='https://t.me/All_animes_in_teluguu_vs')
        ],
        [
            InlineKeyboardButton('❄️ ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('❗ ʜᴇʟᴘ', callback_data='help')
        ]
    ])

    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(message.from_user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(message.from_user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )



@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    if not Config.STRING_SESSION:
        if file.file_size > 2000 * 1024 * 1024:
            return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ")

    try:
        text = f"""**__ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴅᴏ ᴡɪᴛʜ ᴛʜɪs ғɪʟᴇ.?__**\n\n**ғɪʟᴇ ɴᴀᴍᴇ** :- `{filename}`\n\n**ғɪʟᴇ sɪᴢᴇ** :- `{filesize}`"""
        buttons = [
            [InlineKeyboardButton("📝 sᴛᴀʀᴛ ʀᴇɴᴀᴍᴇ 📝", callback_data="rename")],
            [InlineKeyboardButton("✖️ ᴄᴀɴᴄᴇʟ ✖️", callback_data="close")]
        ]
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass



@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data

    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/All_animes_in_teluguu_vs'),
                    InlineKeyboardButton('🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/All_animes_in_teluguu_vs')
                ],
                [
                    InlineKeyboardButton('❄️ ᴀʙᴏᴜᴛ', callback_data='about'),
                    InlineKeyboardButton('❗ ʜᴇʟᴘ', callback_data='help')
                ]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close"),
                    InlineKeyboardButton("⟪ ʙᴀᴄᴋ", callback_data="start")
                ]
            ])
        )

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close"),
                    InlineKeyboardButton("⟪ ʙᴀᴄᴋ", callback_data="start")
                ]
            ])
        )

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
