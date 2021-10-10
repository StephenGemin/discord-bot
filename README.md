
# Discord Bot

[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## About
Discord bot that provides words of encouragement when a predefined word is 
typed in chat

Based on the following:
* [YouTube tutorial](https://www.youtube.com/watch?v=SPTfmiYiuok)

### Installation
1. clone repo
2. `pip install -r requirements.txt`
3. Create `.env` folder in project root directory
4. Create file env.json
5. Add Discord bot token 
   * Ex. "BOT_TOKEN": "DISCORD_BOT_TOKEN_HERE"
6. Follow YouTube tutorial to create Discord account, server and add the bot
7. Run `main.py` script
   * Follow YouTube tutorial if you run into any problems


### Key differences from YouTube video
* Not using Repl.it
  * Just because ...
* Using sqlite database instead of Repl.it database
   * Uses SQLAlchemy. Yes this is completely overkill.  

