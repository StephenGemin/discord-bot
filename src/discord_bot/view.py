import logging
import json
import random
import re
from typing import List

import discord
import requests

from . import constants
from . import models

logger = logging.getLogger(__name__)


def _get_token() -> str:
    with open(str(constants.ENV_FILE), "r") as f_env:
        contents = json.load(f_env)
        return contents["BOT_TOKEN"]


def get_inspirational_quote() -> str:
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)[0]  # single quote returned as a list[dict]
    return f"{json_data['q']}\n\t{json_data['a']}"


def needs_encouragement(message: str, session) -> bool:
    filtered = re.sub(r"[^\w\s]", "", message)
    logger.info(f"Filtered message: {filtered}")
    trigger_words = query_sad_words(session)
    match = any(word in filtered for word in trigger_words)
    logger.info(f"Match: {match}")
    return match


def query_sad_words(session) -> List[str]:
    query = session.query(models.SadTrigger.word).all()
    return [w[0] for w in query]


def query_encourage_words(session) -> List[str]:
    query = session.query(models.SadResponse.response).all()
    return [w[0] for w in query]


def trigger_events(client, db_session):
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        logger.debug(f"New message: {message}")
        logger.info(f"New message: {message.content}")
        if message.author == client.user:
            return

        msg = message.content

        if re.match(r"\$hello", msg, flags=re.IGNORECASE):
            await message.channel.send("Hello, how are you today?")

        if re.match(r"\$inspire", msg, flags=re.IGNORECASE):
            quote = get_inspirational_quote()
            await message.channel.send(quote)

        if needs_encouragement(msg, db_session):
            encourage_responses = query_encourage_words(db_session)
            await message.channel.send(random.choice(encourage_responses))


def start_discord_bot():
    client = discord.Client()
    db_session = models.load_db()
    trigger_events(client, db_session)
    client.run(_get_token())
