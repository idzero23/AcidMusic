"""
MusicRadio, Telegram Voice Chat Bot
Copyright (c) 2021  Artezid Idzeroid <https://github.com/idzero23>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, errors
from AcidMusic.config import AcidMusic.Config

REPLY_MESSAGE=Config.REPLY_MESSAGE
buttons = [
            [
                InlineKeyboardButton("❔ HOW TO USE ME ❔", callback_data="help"),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/ArtezID"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/Idzero_GR"),
            ],
            [
                InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://heroku.com/deploy?template=https://github.com/idzero23/MusicRadio"),
            ]
         ]


@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "IDZE_ROID":
        answers.append(
            InlineQueryResultArticle(
                title="Deploy Your Own Bot Music Stream",
                thumb_url="https://telegra.ph/file/ecce3d02b7acce2a7a022.jpg",
                input_message_content=InputTextMessageContent(f"{REPLY_MESSAGE}\n\n<b>© Powered By : \nARTEZID | IDZEROID</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("Type An Song Name ?"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/play https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Error: Search Timed Out!"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
