import telebot
from telebot import types
import random
six_gifs = [
    "CgACAgQAAyEFAASlWByVAAPLaij_Bk6Y7x5B0Zo_QpRHMYpFqmwAAjMYAAK5EtlTOD9lL9OnblU7BA",
    "CgACAgQAAyEFAASlWByVAAPKaij-wkg3aKnyDQ2PUBeX_L1kXhcAAk8bAAKseChQ1zWY76wEaVc7BA",
    "CgACAgQAAyEFAASlWByVAAPJaij-kJSREFqSppJUVbD79NZVNpoAAjkfAALVfXBQCe29iKUQleU7BA",
    "CgACAgQAAyEFAASlWByVAAPIaij-kKXRTScFKlK-V4XXBgrFg4UAAr4gAAKGA0BQP3EZ4xaQEd87BA",
    "CgACAgQAAyEFAASlWByVAAPHaij-jpDDrDl1iSQdxsQcpHzyzxcAAsAgAAKGA0BQn1P8A9Sr_nQ7BA",
  "CgACAgQAAyEFAASlWByVAAPaaikAAcBeKjxpAaKVNyv9wa0Tc_VCAAL6HAACuRLRUxoNV9iu6BabOwQ",
  
"CgACAgQAAyEFAASlWByVAAPZaikAAbqraavryviBRnefhBj4yg0SAAJMGwACrHgoUGv7DR74vK_iOwQ",
]

last_six_gif = {}

four_gifs = [
  
"CgACAgQAAyEFAASlWByVAAPdaikNMEt1BPaC2ksClR8VfTOgUQIAAoceAAIbHZhQbOx-jletamw7BA",

"CgACAgQAAyEFAASlWByVAAPkaikQ1hCs5qzE3O5y0BRJWcIyDs4AAlEbAAKseChQYmUqDjlqb_Y7BA",

"CgACAgQAAyEFAASlWByVAAPjaikQqErbDyp0aJTKvlDXypqqLoAAAj8eAALqbGBRKrqcXvo6rkk7BA",

"CgACAgQAAyEFAASlWByVAAPiaikQphfdHfB9H6fxgYZofwGenpAAAu4YAAJHjtlRcDGOTaX2LoY7BA",

"CgACAgQAAyEFAASlWByVAAPhaikQoqzrFouqTjsWa0nPTg93XrkAAl0WAAIBEQFT5RwLnrjwcKI7BA",

"CgACAgQAAyEFAASlWByVAAPfaikOptU95l45Bcgn9UVi3lw1eXMAAugeAAKseDBQ8m_Dt_yzKGQ7BA",

]
last_four_gif = {}

TOKEN = "8602786350:AAHdDhPR23-wdw9ixBtAlbdgvcqZ3nZNZC0"

bot = telebot.TeleBot(TOKEN)

scores = {}
balls = {}

# START MENU
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("Profile", "Solo Match")
    markup.row("Team Match", "Leaderboard")
    markup.row("Daily Reward", "Settings")

    bot.send_message(
        message.chat.id,
        "🏏 Welcome to CricketVerse!\n\nChoose an option:",
        reply_markup=markup
    )

# PROFILE
@bot.message_handler(func=lambda m: m.text == "Profile")
def profile(message):
    name = message.from_user.first_name

    bot.send_message(
        message.chat.id,
        f"""🏏 PLAYER PROFILE

Name: {name}

Level: 1
Coins: 1000

Runs: 0
Wickets: 0

Matches: 0

Team: None"""
    )

# SOLO MATCH
@bot.message_handler(func=lambda m: m.text == "Solo Match")
def solo_match(message):

    user_id = message.from_user.id

    scores[user_id] = 0
    balls[user_id] = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("1", "2", "3")
    markup.row("4", "6")

    bot.send_message(
        message.chat.id,
        """🏏 MATCH STARTED

Score: 0
Balls: 0/6

Choose your shot:""",
        reply_markup=markup
    )

# SHOT SYSTEM
@bot.message_handler(func=lambda m: m.text in ["1", "2", "3", "4", "6"])
def shot(message):

    user_id = message.from_user.id

    if user_id not in scores:
        bot.send_message(message.chat.id, "Pehle Solo Match start karo.")
        return

    player_shot = message.text
    bot_ball = random.choice(["1", "2", "3", "4", "6"])

    balls[user_id] += 1

    if player_shot == bot_ball:

        bot.send_message(
            message.chat.id,
            f"""🎯 Bot chose: {bot_ball}

❌ OUT!

Final Score: {scores[user_id]}"""
        )

        del scores[user_id]
        del balls[user_id]
        return

    scores[user_id] += int(player_shot)
    
    if player_shot == "4":

        gif = random.choice(four_gifs)

    while gif == last_four_gif.get(user_id):
        gif = random.choice(four_gifs)

    last_four_gif[user_id] = gif

    bot.send_animation(message.chat.id, gif)

    bot.send_message(
        message.chat.id,
        f"""🔥 FOUR!

What a beautiful boundary!

Score: {scores[user_id]}
Balls: {balls[user_id]}/6"""
    )



    if player_shot == "6":

        gif = random.choice(six_gifs)

        while gif == last_six_gif.get(user_id):
            gif = random.choice(six_gifs)

        last_six_gif[user_id] = gif

        bot.send_animation(message.chat.id, gif)

        bot.send_message(
            message.chat.id,
            f"""🚀 MASSIVE SIX!

Score: {scores[user_id]}
Balls: {balls[user_id]}/6"""
        )

    else:

        bot.send_message(
            message.chat.id,
            f"""🎯 Bot chose: {bot_ball}

🏏 {player_shot} Runs!

Score: {scores[user_id]}
Balls: {balls[user_id]}/6"""
        )
# GIF ID GETTER
@bot.message_handler(content_types=['animation'])
def get_gif_id(message):
    bot.reply_to(
        message,
        f"GIF ID:\n{message.animation.file_id}"
    )

print("Bot Started...")
bot.infinity_polling()
