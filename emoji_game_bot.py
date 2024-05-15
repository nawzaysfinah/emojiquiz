from pyrogram import Client, filters
import random

api_id = "21997526"
api_hash = "9659ac33986a5f7e02d5802dbf3f598e"
bot_token = "7030031183:AAGbWEEZHzpcivCsM3xJN4zaG_rQOtDwF4w"

app = Client("my_emoji_game_bot", bot_token=bot_token, api_id=api_id, api_hash=api_hash)

base_challenges = [
    {"emojis": "🌍🚀", "answer": "space earth"},
    {"emojis": "🍎❤️", "answer": "apple love"},
    {"emojis": "⚪️🐥🐥", "answer": "white chicks"},
    {"emojis": "💩👴", "answer": "dirty grandpa"},
    {"emojis": "🐀👨‍🍳🍲", "answer": "ratatouille"},
    {"emojis": "🧙‍♂️🧹⚡️", "answer": "harry potter"},
    {"emojis": "🚢❄️💔", "answer": "titanic"},
    {"emojis": "👣🥁", "answer": "left toe right toe keep up the tempo"},
    {"emojis": "🫵🤰🟢", "answer": "mak kau hijau"},
    {"emojis": "🦆🌒🔙", "answer": "dark knight returns"},
    {"emojis": "☠️🚕4️⃣🥰", "answer": "death cab for cutie"}
]
games = {}  # Store game states with shuffled challenges for each chat

@app.on_message(filters.command("start"))
async def start_game(client, message):
    chat_id = message.chat.id
    shuffled_challenges = random.sample(base_challenges, len(base_challenges))  # Create a shuffled copy
    games[chat_id] = {'challenges': shuffled_challenges, 'index': 0}
    await message.reply("Welcome to the Emoji Guessing Game! 🎉 Are you ready to play? Send /play to start!")

@app.on_message(filters.command("play"))
async def send_challenge(client, message):
    chat_id = message.chat.id
    if chat_id not in games:
        await start_game(client, message)  # Correctly await coroutine
    else:
        await send_next_challenge(message, chat_id)

async def send_next_challenge(message, chat_id):
    game = games[chat_id]
    challenge = game['challenges'][game['index']]['emojis']
    await message.reply(f"Guess what this means: {challenge}")

@app.on_message(filters.text)
async def check_answer(client, message):
    chat_id = message.chat.id
    if message.text.startswith('/'):
        return  # Ignore commands
    if chat_id in games:
        game = games[chat_id]
        user_response = message.text.lower().strip()
        correct_answer = game['challenges'][game['index']]['answer']
        if user_response == correct_answer:
            game['index'] += 1
            if game['index'] < len(game['challenges']):
                await message.reply("Correct! 🎉 Here's the next one:")
                await send_next_challenge(message, chat_id)
            else:
                await message.reply("Congratulations, you've completed all challenges!")
                games.pop(chat_id)  # Remove game state when finished
        else:
            await message.reply("That's not quite right. Try again or send /skip to move to the next one.")

@app.on_message(filters.command("skip"))
async def skip_challenge(client, message):
    chat_id = message.chat.id
    if chat_id in games:
        game = games[chat_id]
        game['index'] += 1
        if game['index'] < len(game['challenges']):
            await send_next_challenge(message, chat_id)
        else:
            await message.reply("No more challenges to skip to! You've reached the end.")
            games.pop(chat_id)  # Remove game state when finished

if __name__ == "__main__":
    app.run()
