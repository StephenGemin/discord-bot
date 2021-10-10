from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
APP_NAME = "discord_bot"
ENV_DIR = PROJECT_DIR.joinpath(".env")
ENV_FILE = ENV_DIR.joinpath("env.json")
ROOT = PROJECT_DIR.joinpath(APP_NAME)
DATA_DIR = ROOT.joinpath("data")
DB_NAME = "discord_bot.db"
