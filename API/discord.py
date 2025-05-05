import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# TODO: Implement discord API
# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")  # Path to ffmpeg executable

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Voice client
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to join a voice channel first!")


@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")


@bot.command(name="play")
async def play(ctx, file_id: str):
    if not ctx.voice_client:
        await ctx.send("Join a voice channel first using `!join`.")
        return

    # Download file from cloud
    audio_file = download_file(file_id)  # TODO: Implement this function
    if not audio_file:
        await ctx.send("Could not find the audio file.")
        return

    # Play the audio
    source = discord.FFmpegPCMAudio(audio_file, executable=FFMPEG_PATH)
    ctx.voice_client.play(source, after=lambda e: print(f"Finished playing: {e}"))
    await ctx.send(f"Playing: {file_id}")


# Run the bot
bot.run(TOKEN)
