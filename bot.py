import os
import discord
from discord import app_commands
from discord.ext import commands

# Intents (only need default guilds intent here)
intents = discord.Intents.default()

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Read env vars or replace here
DISCORD_TOKEN = os.getenv("MTM5MzkyNDYxODM3MjUxMzkzMg.GOpdd9.RaYlYKAPftGZp1EpGWz3RVXxOLfcMrB2fcVUxI")
CHANNEL_ID = int(os.getenv("1330295535986282506"))
BANNER_URL = os.getenv("BANNER_URL", "https://media.discordapp.net/attachments/1330290790924292182/1393883913901969408/getinto.png?ex=6874cb0e&is=6873798e&hm=a0da7ecf1a533a5b861f7fdff96570cc7581e7f6f9bd16c368e2bdfd1cfe34e1&=&format=webp&quality=lossless&width=2500&height=939")

# Define the slash command tree
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="timetable_claim", description="Claim a teaching timetable slot")
@app_commands.describe(
    name="Your teaching name",
    year="Year to teach (e.g., Year 10)",
    subject="Subject",
    room="Room (e.g., R2)"
)
async def timetable_claim(interaction: discord.Interaction, name: str, year: str, subject: str, room: str):
    embed = discord.Embed(
        title="📝 Timetable Claim",
        color=discord.Color.red()
    )
    embed.add_field(name="Teaching Name", value=name, inline=True)
    embed.add_field(name="Year to Teach", value=year, inline=True)
    embed.add_field(name="Subject", value=subject, inline=True)
    embed.add_field(name="Room", value=room, inline=True)
    embed.set_footer(text=" ", icon_url=BANNER_URL)

    # Send to channel
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        await interaction.response.send_message("❌ Error: Claim channel not found.", ephemeral=True)
        return

    await channel.send(embed=embed)

    # DM the user a confirmation
    try:
        await interaction.user.send("✅ Your claim has been posted!", embed=embed)
    except discord.Forbidden:
        # Can't DM user (privacy settings)
        pass

    await interaction.response.send_message("✅ Your claim has been posted! Check your DMs.", ephemeral=True)

# Run bot
bot.run(DISCORD_TOKEN)
