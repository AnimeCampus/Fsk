import requests
from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Replace with your actual bot username
BOT_USERNAME = "GeniusHubMusicBot"

# Function to shorten a URL using easysky.in API
def shorten_url(url):
    api_key = "26900f01070d5c9fcdd9ece883701597c9b302c1"
    api_url = f"https://easysky.in/api/v1/shorten?key={api_key}&url={url}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        short_url = response.json().get("short_link")
        return short_url
    else:
        return None

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="<b>Please Forward the First Message/File from Channel DataBase. (Forward with Quote)\n\nor Send Post Link from Channel Database</b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except BaseException:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        await first_message.reply(
            "❌ <b>ERROR</b>\n\n<b>This Forwarded post is not from my Channel Database</b>",
            quote=True,
        )
        continue

    while True:
        try:
            second_message = await client.ask(
                text="<b>Please Forward the Second Message/File from Channel DataBase. (Forward with Quote)\n\nor Send Post Link from Channel Database</b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except BaseException:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        await second_message.reply(
            "❌ <b>ERROR</b>\n\n<b>This Forwarded post is not from my Channel Database</b>",
            quote=True,
        )
        continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    shortened_link = shorten_url(link)
    
    if shortened_link:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔁 Share Link", url=f"https://telegram.me/share/url?url={shortened_link}"
                    )
                ]
            ]
        )
        await second_message.reply_text(
            f"<b>Shortened link sharing file successfully created:</b>\n\n{shortened_link}",
            quote=True,
            reply_markup=reply_markup,
        )
    else:
        await second_message.reply_text(
            "❌ <b>ERROR</b>\n\n<b>Failed to create shortened link</b>",
            quote=True,
        )

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("genlink"))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="<b>Please Forward the last Message/File from Channel DataBase. (Forward with Quote)\n\nor Send Post Link from Channel Database</b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except BaseException:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        await channel_message.reply(
            "❌ <b>ERROR</b>\n\n<b>This Forwarded post is not from my Channel Database</b>",
            quote=True,
        )
        continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    shortened_link = shorten_url(link)
    
    if shortened_link:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔁 Share Link", url=f"https://telegram.me/share/url?url={shortened_link}"
                    )
                ]
            ]
        )
        await channel_message.reply_text(
            f"<b>Shortened link sharing file successfully created:</b>\n\n{shortened_link}",
            quote=True,
            reply_markup=reply_markup,
        )
    else:
        await channel_message.reply_text(
            "❌ <b>ERROR</b>\n\n<b>Failed to create shortened link</b>",
            quote=True,
        )

