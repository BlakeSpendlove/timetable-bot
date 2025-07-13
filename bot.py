import os
import discord
from discord import app_commands
from discord.ext import commands

# Load variables from Railway environment
DISCORD_TOKEN = os.getenv("MTM5MzkyNDYxODM3MjUxMzkzMg.GOpdd9.RaYlYKAPftGZp1EpGWz3RVXxOLfcMrB2fcVUxI")
CHANNEL_ID = int(os.getenv("https://discord.com/channels/1329883087378845747/1330295535986282506"))
BANNER_URL = os.getenv("BANNER_URL", "https://media.discordapp.net/attachments/1330290790924292182/1393883913901969408/getinto.png?ex=6874cb0e&is=6873798e&hm=a0da7ecf1a533a5b861f7fdff96570cc7581e7f6f9bd16c368e2bdfd1cfe34e1&=&format=webp&quality=lossless&width=2500&height=939")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

@bot.tree.command(name="timetable_claim", description="Claim a teaching timetable slot")
@app_commands.describe(
    name="Your teaching name",
    year="Year group to teach",
    subject="The subject",
    room="Room to teach in"
)
async def claim(interaction: discord.Interaction, name: str, year: str, subject: str, room: str):
    embed = discord.Embed(title="📝 Timetable Claim", color=discord.Color.red())
    embed.add_field(name="Teaching Name", value=name, inline=True)
    embed.add_field(name="Year to Teach", value=year, inline=True)
    embed.add_field(name="Subject", value=subject, inline=True)
    embed.add_field(name="Room", value=room, inline=True)
    embed.set_footer(text=" ", icon_url=BANNER_URL)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)

    await interaction.response.send_message("✅ Your lesson has been claimed!", ephemeral=True)

bot.run(DISCORD_TOKEN)
