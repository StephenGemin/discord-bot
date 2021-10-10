import logging
import json
import random
import re

import discord
import requests

import constants
import models

logging.basicConfig(level=logging.INFO)


def _get_token() -> str:
    env_file = constants.ENV_DIR.joinpath(".env.json")
    with open(str(env_file), "r") as f_env:
        contents = json.load(f_env)
        return contents["BOT_TOKEN"]


def get_inspirational_quote() -> str:
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)[0]  # single quote returned as a list[dict]
    return f"{json_data['q']}\n\t{json_data['a']}"


def needs_encouragement(session, message) -> bool:
    filtered = re.sub(r"[^\w\s]", "", message)
    logging.info(f"Filtered message: {filtered}")
    query = session.query(models.SadTrigger.word).all()
    sad_words = [w[0] for w in query]
    match = any(word in filtered for word in sad_words)
    logging.info(f"Match: {match}")
    return match


def trigger_events(client, db_session):
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        logging.debug(f"New message: {message}")
        logging.info(f"New message: {message.content}")
        if message.author == client.user:
            return

        msg = message.content

        if re.match(r"\$.hello", msg, flags=re.IGNORECASE):
            await message.channel.send("Hello, how are you today?")

        if re.match(r"\$.inspire", msg, flags=re.IGNORECASE):
            quote = get_inspirational_quote()
            await message.channel.send(quote)

        if needs_encouragement(db_session, msg):
            query = db_session.query(models.SadResponse.response).all()
            encourage_responses = [w[0] for w in query]
            await message.channel.send(random.choice(encourage_responses))


def main():
    client = discord.Client()
    db_session = models.load_db()
    trigger_events(client, db_session)
    client.run(_get_token())


if __name__ == "__main__":
    main()