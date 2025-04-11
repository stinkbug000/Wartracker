import discord
from discord.ext import commands
import json
import os

# Your server IDs
ALLOWED_GUILD_IDS = [1359628998212194596, 1306087142174363690]  # replace with your actual server IDs

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'data.json'

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
else:
    data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

def is_allowed(ctx):
    return ctx.guild and ctx.guild.id in ALLOWED_GUILD_IDS

@bot.command()
async def add(ctx, player: str, stars: int, three_star: bool):
    if not is_allowed(ctx):
        return
    player = player.lower()
    if player not in data:
        data[player] = {"stars": 0, "three_stars": 0, "attacks": 0, "missed": 0}
    data[player]["stars"] += stars
    data[player]["three_stars"] += int(three_star)
    data[player]["attacks"] += 1
    save_data()
    await ctx.send(f"{player} added: {stars} star(s), 3-star: {three_star}")

@bot.command()
async def remove(ctx, player: str, stars: int, three_star: bool):
    if not is_allowed(ctx):
        return
    player = player.lower()
    if player in data:
        data[player]["stars"] -= stars
        data[player]["three_stars"] -= int(three_star)
        data[player]["attacks"] -= 1
        save_data()
        await ctx.send(f"{player} removed: {stars} star(s), 3-star: {three_star}")
    else:
        await ctx.send(f"{player} not found.")

@bot.command()
async def missed(ctx, player: str):
    if not is_allowed(ctx):
        return
    player = player.lower()
    if player not in data:
        data[player] = {"stars": 0, "three_stars": 0, "attacks": 0, "missed": 0}
    data[player]["missed"] += 1
    save_data()
    await ctx.send(f"{player} marked as missed attack.")

@bot.command()
async def batch(ctx, *, message: str):
    if not is_allowed(ctx):
        return
    lines = message.strip().split('\n')
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            player, stars, three_star = parts
            player = player.lower()
            stars = int(stars)
            three_star = three_star.lower() == 'true'
            if player not in data:
                data[player] = {"stars": 0, "three_stars": 0, "attacks": 0, "missed": 0}
            data[player]["stars"] += stars
            data[player]["three_stars"] += int(three_star)
            data[player]["attacks"] += 1
    save_data()
    await ctx.send("Batch update complete.")

@bot.command()
async def summary(ctx):
    if not is_allowed(ctx):
        return
    if not data:
        await ctx.send("No data available.")
        return
    lines = []
    for player, stats in data.items():
        lines.append(
            f"**{player.title()}** - Stars: {stats['stars']}, "
            f"3-stars: {stats['three_stars']}, "
            f"Attacks: {stats['attacks']}, "
            f"Missed: {stats['missed']}"
        )
    await ctx.send("\n".join(lines))

# Start the bot
bot.run(os.getenv("MTM1OTU2MzAwMzQxODI0NzIyOQ.GjGf1E.p1vTdmsOpomgw-Uqj8S5LVaLtFglFhEDL3VE5I"))