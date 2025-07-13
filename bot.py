import discord
from discord import app_commands
from discord.ext import commands
import random
import string
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def generate_claim_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is ready as {bot.user}.")

@bot.tree.command(name="timetable_claim", description="Claim a lesson in the timetable.")
@app_commands.describe(
    teaching_name="Your display name (e.g. Mr Smith)",
    year="Year group being taught (e.g. Year 9)",
    period="Period (e.g. Form, Period 1–5)",
    subject="The subject you're teaching",
    room="Room location (e.g. A1)"
)
async def timetable_claim(interaction: discord.Interaction, teaching_name: str, year: str, period: str, subject: str, room: str):
    await interaction.response.defer(ephemeral=True)

    claim_id = generate_claim_id()
    date_today = datetime.now().strftime("%d/%m/%Y")

    embed = discord.Embed(
        title="📚 New Timetable Claim",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="👨‍🏫 Teaching Name", value=teaching_name, inline=False)
    embed.add_field(name="🏫 Year Group", value=year, inline=True)
    embed.add_field(name="⏰ Period", value=period, inline=True)
    embed.add_field(name="📘 Subject", value=subject, inline=True)
    embed.add_field(name="🏢 Room", value=room, inline=True)
    embed.set_footer(text=f"Claim ID: {claim_id} • Date: {date_today}")
    embed.set_image(url="https://example.com/banner.png")  # Replace this with your actual banner URL

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(content=f"📢 {interaction.user.mention} has claimed a timetable slot!", embed=embed)
        await interaction.followup.send("✅ Your timetable claim has been posted!", ephemeral=True)
    else:
        await interaction.followup.send("❌ Couldn't find the target channel.", ephemeral=True)

bot.run(TOKEN)
