import discord
from discord.ext import commands
import random
import json
import os

# === Load config.json ===
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["token"]
PREFIX = config.get("prefix", "?")
CHEAT_FILE = "cheats.json"

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.default())

# === Helpers for cheats.json ===
def load_cheats():
    if not os.path.exists(CHEAT_FILE):
        return {}
    try:
        with open(CHEAT_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_cheats(data):
    with open(CHEAT_FILE, "w") as f:
        json.dump(data, f)

cheats = load_cheats()  # dict[user_id -> "heads"/"tails"/"random"/"off"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# === Rig command ===
@bot.command(name="rigme")
async def rigme(ctx, choice: str):
    choice = choice.lower()
    allowed = ("heads", "tails", "random", "off")
    if choice not in allowed:
        await ctx.send("Usage: `?rigme heads | tails | random | off`")
        return

    uid = str(ctx.author.id)
    if choice == "off":
        cheats.pop(uid, None)
        save_cheats(cheats)
        await ctx.send(f"{ctx.author.mention}, your rig has been turned **off**.")
        return

    cheats[uid] = choice
    save_cheats(cheats)
    await ctx.send(f"{ctx.author.mention}, you are now rigged to **{choice.capitalize()}**.")

# === Check rig status ===
@bot.command(name="myrig")
async def myrig(ctx):
    uid = str(ctx.author.id)
    val = cheats.get(uid, "off")
    await ctx.send(f"{ctx.author.mention}, your rig: **{val}**")

# === Coinflip ===
@bot.command(name="flip")
async def flip(ctx):
    uid = str(ctx.author.id)
    user_choice = cheats.get(uid, "random")

    if user_choice in ("heads", "tails"):
        outcome = "Heads" if user_choice == "heads" else "Tails"
    else:
        outcome = random.choice(["Heads", "Tails"])

    # Random embed color (red, yellow, blue)
    colors = [discord.Color.red(), discord.Color.gold(), discord.Color.blue()]
    embed_color = random.choice(colors)

    embed = discord.Embed(
        description=f"{ctx.author.name} flipped a coin and got **{outcome}**",
        color=embed_color
    )
    embed.set_footer(text="You can now change carl-bot profile picture and banner with premium!!")

    await ctx.send(embed=embed)

# === Run bot ===
bot.run(TOKEN)
