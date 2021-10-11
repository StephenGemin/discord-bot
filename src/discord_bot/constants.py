from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
ENV_DIR = PACKAGE_DIR.joinpath(".env")
ENV_FILE = ENV_DIR.joinpath("env.json")

APP_NAME = "discord_bot"
DB_NAME = "discord_bot.db"
