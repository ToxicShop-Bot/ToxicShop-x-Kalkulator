import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ========================
# KONFIGURACJA
# ========================

KURS = 1000  # ile waluty za 1 PLN


# ========================
# VIEW (PRZYCISKI)
# ========================

class KalkulatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ile otrzymam?", style=discord.ButtonStyle.green)
    async def ile_otrzymam(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OtrzymamModal())

    @discord.ui.button(label="Ile muszę dać?", style=discord.ButtonStyle.blurple)
    async def ile_musze_dac(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MuszeDacModal())


# ========================
# MODALE
# ========================

class OtrzymamModal(discord.ui.Modal, title="ToxicShop x Bot - Kalkulator"):
    kwota = discord.ui.TextInput(label="Podaj kwotę w PLN (min. 10 zł)", placeholder="Np. 50")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            pln = float(self.kwota.value)

            if pln < 10:
                await interaction.response.send_message("❌ Minimalna kwota to 10 zł.", ephemeral=True)
                return

            wynik = pln * KURS
            await interaction.response.send_message(
                f"💰 Za **{pln} zł** otrzymasz **{int(wynik):,}** waluty.",
                ephemeral=True
            )
        except:
            await interaction.response.send_message("❌ Podaj poprawną liczbę.", ephemeral=True)


class MuszeDacModal(discord.ui.Modal, title="ToxicShop x Bot - Kalkulator"):
    waluta = discord.ui.TextInput(label="Ile waluty chcesz otrzymać?", placeholder="Np. 50000")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            waluta = float(self.waluta.value)

            pln = waluta / KURS

            if pln < 10:
                pln = 10

            await interaction.response.send_message(
                f"💰 Aby otrzymać **{int(waluta):,}** waluty, musisz zapłacić około **{pln:.2f} zł**.\n"
                f"📌 Minimalna kwota to 10 zł.",
                ephemeral=True
            )
        except:
            await interaction.response.send_message("❌ Podaj poprawną liczbę.", ephemeral=True)


# ========================
# KOMENDA
# ========================

@bot.command()
async def kalkulator(ctx):
    embed = discord.Embed(
        title="📦 TOXICSHOP x KALKULATOR",
        description=(
            "Szybko oblicz:\n"
            "• ile otrzymasz waluty za określoną ilość PLN\n"
            "• ile musisz zapłacić za daną ilość waluty\n\n"
            "Minimalna kwota: **10 zł**"
        ),
        color=0x2b2d31
    )

    embed.set_image(url="TUTAJ_WKLEJ_LINK_DO_BANERA")

    await ctx.send(embed=embed, view=KalkulatorView())


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    bot.add_view(KalkulatorView())


bot.run(TOKEN)
