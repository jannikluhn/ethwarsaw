from dotenv import load_dotenv

load_dotenv()

import asyncio
import logging
import json
import os
import redis.asyncio as redis
import requests
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)
import yaml
from web3 import Web3, HTTPProvider

NEW_ENCOUNTERS_CHANNEL_NAME = "newEncounters"
NEW_GAME_ANSWERS_CHANNEL_NAME = "newGameAnswer"
APPROACH_OPTION = "approach"
IGNORE_OPTION = "ignore"
HELP_OPTION = "help"
FLUFFEVERSE_OPTION = "fluffeverse"

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DIALOGUE_PATH = os.environ["DIALOGUE_PATH"]
GAME_URL = os.environ["GAME_URL"]
CELO_RPC_URL = os.environ["CELO_RPC_URL"]
MANTLE_RPC_URL = os.environ["MANTLE_RPC_URL"]
CELO_CONTRACT_ADDRESS = os.environ["CELO_CONTRACT_ADDRESS"]
MANTLE_CONTRACT_ADDRESS = os.environ["MANTLE_CONTRACT_ADDRESS"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

with open("abi.json") as f:
    CONTRACT_ABI = json.load(f)


def load_dialogue():
    with open(DIALOGUE_PATH) as f:
        return yaml.safe_load(f)


dialogue = load_dialogue()

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def make_user_key(address):
    return f"user:{address}"


def make_chat_secret_key(chat_secret):
    return f"userChatSecret:{chat_secret}"


def make_chat_id_address_key(chat_id):
    return f"chatIdAddress:{chat_id}"


def make_user_encounters_key(address):
    return f"userEncounters:{address}"


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=dialogue["unknown"]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_secret = context.args[0]
    chat_secret_key = make_chat_secret_key(chat_secret)
    address = await r.hget(chat_secret_key, "address")

    if not address:
        await update.message.reply_text(text=dialogue["invalid_chat_secret"])
        return

    user_key = make_user_key(address)
    await r.hset(user_key, "chatId", str(update.message.chat_id))

    chat_id_address_key = make_chat_id_address_key(update.message.chat_id)
    await r.set(chat_id_address_key, address)

    keyboard = [
        [
            InlineKeyboardButton("Fluffeverse", callback_data=FLUFFEVERSE_OPTION),
            InlineKeyboardButton("Help", callback_data=HELP_OPTION),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=dialogue["welcome"], reply_markup=reply_markup)


async def creatures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    chat_id_address_key = make_chat_id_address_key(chat_id)
    address = await r.get(chat_id_address_key)

    for contract_address, rpc_url in [
        [MANTLE_CONTRACT_ADDRESS, MANTLE_RPC_URL],
        [CELO_CONTRACT_ADDRESS, CELO_RPC_URL],
    ]:
        w3 = Web3(HTTPProvider(rpc_url))
        c = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
        n = c.functions.balanceOf(address).call()
        if n > 0 or True:
            uri = c.functions.tokenURI(n - 1).call()
            metadata = requests.get(uri).json()
            ipfs_hash = metadata["image"]
            image_url = "https://ipfs.io/ipfs/" + ipfs_hash[7:]
            await update.message.reply_photo(image_url)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    if query.data == IGNORE_OPTION:
        return await ignore_encounter(update, context)
    elif query.data == APPROACH_OPTION:
        return await approach_encounter(update, context)
    elif query.game_short_name == "CreatureEncounter":
        return await start_game(update, context)
    elif query.data == FLUFFEVERSE_OPTION:
        return await fluffeverse(update, context)
    elif query.data == HELP_OPTION:
        return await show_help(update, context)
    else:
        raise ValueError("unhandled callback")


async def ignore_encounter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await update.effective_chat.send_message(dialogue["ignored_encounter"])


async def fluffeverse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await update.effective_chat.send_message(dialogue["fluffeverse"])


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await update.effective_chat.send_message(dialogue["help"])


async def approach_encounter(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    address = await r.get(make_chat_id_address_key(update.effective_chat.id))
    latest_encounter_key = await r.lindex(make_user_encounters_key(address), -1)
    if not latest_encounter_key:
        await update.effective_chat.send_message(dialogue["no_encounter_found"])
        return

    encounter = await r.hgetall(latest_encounter_key)
    if not encounter:
        await update.effective_chat.send_message(dialogue["no_encounter_found"])
        return

    game_url = GAME_URL + encounter["game"][5:]
    # game_url = GAME_URL + "game:42220:21192556:13"[5:]
    await update.effective_chat.send_message(
        f"As soon as you're ready, click on the link to try and adopt the creature: {game_url}"
    )


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    address = await r.get(make_chat_id_address_key(update.effective_chat.id))
    latest_encounter_key = await r.lindex(make_user_encounters_key(address), -1)
    if not latest_encounter_key:
        await query.answer()
        await update.effective_chat.send_message(dialogue["no_encounter_found"])
        return

    encounter = await r.hgetall(encounter_key)
    if not encounter:
        await query.answer()
        await update.effective_chat.send_message(dialogue["no_encounter_found"])
        return
    print(encounter)

    game_url = GAME_URL + encounter["game"][5:]
    # game_url = GAME_URL + "game:42220:21192556:13"[5:]
    await query.answer(url=game_url)


async def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("creatures", creatures))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(CallbackQueryHandler(button))

    # try:
    try:
        await app.initialize()
        await app.updater.start_polling()
        await app.start()
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


async def listen_redis():
    pubsub = r.pubsub()
    bot = Bot(TELEGRAM_BOT_TOKEN)

    # Subscribe to a channel (or multiple channels)
    await pubsub.subscribe(NEW_ENCOUNTERS_CHANNEL_NAME)

    # Listen for messages
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(NEW_ENCOUNTERS_CHANNEL_NAME)

        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                await handle_redis_message(bot, message)


async def handle_redis_message(bot, message):
    if message["channel"] == NEW_ENCOUNTERS_CHANNEL_NAME:
        await handle_new_encounter(bot, message["data"])
    elif message["channel"] == NEW_GAME_ANSWERS_CHANNEL_NAME:
        await handle_new_game_answer(bot, message["data"])
    else:
        logging.warn("received redis message on unexpected channel")


async def handle_new_encounter(bot, encounter_key):
    encounter = await r.hgetall(encounter_key)
    user = await r.hgetall(encounter["user"])
    chat_id = int(user["chatId"])
    # chat_id = 3227118
    keyboard = [
        [
            InlineKeyboardButton("Approach", callback_data=APPROACH_OPTION),
            InlineKeyboardButton("Ignore", callback_data=IGNORE_OPTION),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(
        chat_id,
        dialogue["encounter"],
        reply_markup=reply_markup.to_dict(),
    )


async def handle_new_game_answer(bot, encounter_key):
    encounter = await r.hgetall(encounter_key)
    user = await r.hgetall(encounter["user"])
    chat_id = int(user["chatId"])
    # chat_id = 3227118
    game = await r.hgetall(encounter["game"])
    if game["answer"] == game["correctAnswer"]:
        await bot.send_message(
            chat_id,
            dialogue["successful_adoption"],
        )
    else:
        await bot.send_message(
            chat_id,
            dialogue["failed_adoption"],
        )


async def main():
    await asyncio.gather(run_bot(), listen_redis())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
