# Downloads Organizer

Sorts your Downloads folder into categories (Images, Documents, Videos, Archives, Programs, Others).
Can be controlled from your phone through a Telegram bot running on your PC.

## Commands

- `/myid` - shows your Telegram user ID
- `/report` - counts files per category
- `/preview` - shows what would be moved (nothing is changed)
- `/organize` - moves the files into category folders

Only the user ID set in `.env` can run the commands.

## Setup

1. Install the requirements:

```
pip install -r requirements.txt
```

2. Create a bot with @BotFather and copy its token.
3. Create a `.env` file next to `bot.py`:

```
BOT_TOKEN=your_token_here
ALLOWED_USER_ID=your_telegram_id
```

4. Run the bot:

```
python bot.py
```

Note: if Telegram is blocked in your country, set a proxy in `bot.py` (the `PROXY` variable).