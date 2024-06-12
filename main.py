import discord
import os
import time
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
from typing import Final

# load token from secure location
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# set intents and create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="?", intents=intents)


# bot online notification (backend)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online!")
    return



# commands

# ping command (for testing purposes)
@bot.command(name="ping", pass_context=True)
async def ping(ctx):
    await ctx.send(f"Latency: {round(bot.latency * 1000)} ms")
    return

# command that creates an embed of uids for gacha games (genshin, honkai star rail, etc)
@bot.command(name="embed_uids", pass_context=True)
@has_permissions(administrator=True)
async def embed_uids(ctx):
    # get the UIDS and the discord user they belong to
    uids = {}
    async for msg in ctx.channel.history(limit=100):
        user = msg.author
        uid = msg.content
        uids[user] = uid
    # add them to an embed
    embed = discord.Embed(title="User IDS", description="An embed that contains user ids for a gacha game, created by an admin user", color=discord.Color.random())
    embed.set_thumbnail(url=f"{ctx.author.display_avatar}")
    for user, uid in uids.items():
        embed.add_field(name=f"{user} UID", value=f"{uid}", inline=True)
    embed.set_footer(text=f"Embed created by {ctx.author}")
    # send the embed
    await ctx.send(embed=embed)

# triggered if the user calling embed_uids doesn't have permissions
@embed_uids.error
async def embed_uids_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Sorry, @{ctx.author.mention}, you do not have permission to use that command.")
    return

@bot.command(name="nuke_channel", pass_context=True)
@has_permissions(administrator=True, manage_messages=True)
async def nuke_channel(ctx):
    # notify the user of what's to come
    await ctx.send("Nuking channel in 3 seconds \nIt's probably gonna take a bit because I can only delete 1 message per second")
    time.sleep(3)
    # default case
    async for msg in ctx.channel.history(limit=500):
        await msg.delete()
        time.sleep(1)
    return

# triggered if the user calling nuke_channel doesn't have permissions
@nuke_channel.error
async def nuke_channel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Sorry, {ctx.author.mention}, you do not have permission to use that command.")
    return

# example slash command
@bot.tree.command(name="ping", description="returns latency to the discord API")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Latency: {round(bot.latency * 1000)} ms")
    return

bot.run(TOKEN)
