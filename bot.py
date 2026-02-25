import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# KONFIGURACJA
# ==========================

MIN_ZAKUP = 10  # minimalna kwota

# ==========================
# KOMENDA
# ==========================

@bot.command()
async def przelicz(ctx, pln: float):

    if pln < MIN_ZAKUP:
        await ctx.send("❌ Minimalny zakup to 10 PLN!")
        return

    # Ustalanie kursu
    if pln >= 200:
        kurs = 5500
    elif pln >= 100:
        kurs = 5000
    else:
        kurs = 4500

    wynik = pln * kurs

    embed = discord.Embed(
        title="💰 Kalkulator ToxicShop",
        color=discord.Color.green()
    )

    embed.add_field(name="💵 Kwota (PLN)", value=f"{pln} zł", inline=False)
    embed.add_field(name="📈 Kurs", value=f"{kurs} za 1 zł", inline=False)
    embed.add_field(name="🪙 Otrzymasz", value=f"{int(wynik):,}".replace(",", " "), inline=False)

    await ctx.send(embed=embed)

# ==========================
# START BOTA
# ==========================

bot.run(TOKEN)
