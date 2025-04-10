import discord
from discord.ext import commands

# Initialize bot with a prefix for commands
bot = commands.Bot(command_prefix='!')

# Define allowed channel IDs (replace these with your actual channel IDs)
ALLOWED_CHANNELS = [123456789012345678, 987654321098765432]  # Replace with your channel IDs

# This will store attack information
attack_data = {}

# Event when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Function to check if the bot is in an allowed channel
async def is_allowed_channel(ctx):
    if ctx.channel.id not in ALLOWED_CHANNELS:
        await ctx.send(f"Sorry, I can't respond in this channel.")
        return False
    return True

# Command to add a single attack
@bot.command()
async def attack(ctx, player: str, war: str, attacks: int):
    if not await is_allowed_channel(ctx):
        return

    # Store or update the attack count for a player in a specific war
    if player not in attack_data:
        attack_data[player] = {}
    if war not in attack_data[player]:
        attack_data[player][war] = {'attacks': 0, 'misses': 0}

    attack_data[player][war]['attacks'] += attacks
    await ctx.send(f"Player {player} has {attack_data[player][war]['attacks']} attacks in {war}.")

# Command to add multiple batch attacks (batch command)
@bot.command()
async def batch(ctx, *args):
    if not await is_allowed_channel(ctx):
        return

    # Expect input like "player_name attacks war_name, ..."
    for attack_info in args:
        player, attacks, war = attack_info.split()
        attacks = int(attacks)  # Convert to integer
        await attack(ctx, player, war, attacks)

# Command to remove a member's attacks in a specific war
@bot.command()
async def remove(ctx, player: str, war: str):
    if not await is_allowed_channel(ctx):
        return

    if player in attack_data and war in attack_data[player]:
        del attack_data[player][war]
        await ctx.send(f"Removed all attacks for {player} in {war}.")
    else:
        await ctx.send(f"No data found for {player} in {war}.")

# Command to report the attack summary (total attacks and misses)
@bot.command()
async def summary(ctx):
    if not await is_allowed_channel(ctx):
        return

    summary_msg = "Attack Summary:\n"
    for player, wars in attack_data.items():
        total_attacks = sum(war_data['attacks'] for war_data in wars.values())
        total_misses = sum(war_data['misses'] for war_data in wars.values())
        summary_msg += f"{player}: {total_attacks} attacks, {total_misses} misses\n"
    await ctx.send(summary_msg)

# Run the bot using the token from environment variables
bot.run('MTM1OTU2MzAwMzQxODI0NzIyOQ.GjGf1E.p1vTdmsOpomgw-Uqj8S5LVaLtFglFhEDL3VE5I')