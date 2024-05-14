from pyrogram import Client, filters

api_id = "21997526"
api_hash = "9659ac33986a5f7e02d5802dbf3f598e"
bot_token = "7030031183:AAGbWEEZHzpcivCsM3xJN4zaG_rQOtDwF4w"

app = Client("my_emoji_game_bot", bot_token=bot_token, api_id=api_id, api_hash=api_hash)

challenges = [
    {"emojis": "🌍🚀", "answer": "space earth"},
    {"emojis": "🍎❤️", "answer": "apple love"},
    # Add more challenges here
]
current_challenge = {}

@app.on_message(filters.command("start"))
async def start_game(client, message):
    await message.reply("Welcome to the Emoji Guessing Game! 🎉 Are you ready to play? Send /play to start!")

@app.on_message(filters.command("play"))
async def send_challenge(client, message):
    user_id = message.from_user.id
    current_challenge[user_id] = 0  # Initialize or reset the challenge index
    await send_next_challenge(message, user_id)

async def send_next_challenge(message, user_id):
    challenge_index = current_challenge[user_id]
    challenge = challenges[challenge_index]["emojis"]
    await message.reply(f"Guess what this means: {challenge}")

@app.on_message(filters.text)
async def check_answer(client, message):
    user_id = message.from_user.id
    if message.text.startswith('/'):
        return  # Ignore commands in the answer checking function
    if user_id in current_challenge:
        user_response = message.text.lower().strip()
        correct_answer = challenges[current_challenge[user_id]]["answer"]
        if user_response == correct_answer:
            current_challenge[user_id] += 1  # Move to the next challenge
            if current_challenge[user_id] < len(challenges):
                await message.reply("Correct! 🎉 Here's the next one:")
                await send_next_challenge(message, user_id)
            else:
                await message.reply("Congratulations, you've completed all challenges!")
                current_challenge.pop(user_id)  # Remove user from current_challenge when done
        else:
            await message.reply("That's not quite right. Try again or send /skip to move to the next one.")

@app.on_message(filters.command("skip"))
async def skip_challenge(client, message):
    user_id = message.from_user.id
    if user_id in current_challenge:
        current_challenge[user_id] += 1
        if current_challenge[user_id] < len(challenges):
            await send_next_challenge(message, user_id)
        else:
            await message.reply("No more challenges to skip to! You've reached the end.")
            current_challenge.pop(user_id)  # Remove user from current_challenge when done

if __name__ == "__main__":
    app.run()
