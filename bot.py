import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== KONFIG =====
MIN_PROWIZJA = 10

METODY = {
    "BLIK (5%)": 0.05,
    "KOD BLIK (10%)": 0.10,
    "PAYPAL (10%)": 0.10,
    "PSC Z PARAGONEM (15%)": 0.15,
    "PSC BEZ PARAGONU (25%)": 0.25,
}

# ===== KURS DOLARÓW =====
def pobierz_kurs(kwota):
    if kwota >= 200:
        return 5500
    elif kwota >= 100:
        return 5000
    else:
        return 4500


# ===== PRZYCISKI GŁÓWNE =====
class KalkulatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ile otrzymam?", style=discord.ButtonStyle.green)
    async def ile_otrzymam(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IleOtrzymamModal())

    @discord.ui.button(label="Ile muszę dać?", style=discord.ButtonStyle.blurple)
    async def ile_musze_dac(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IleMuszeDacModal())


# ===== MODAL 1 =====
class IleOtrzymamModal(discord.ui.Modal, title="Ile otrzymam?"):
    kwota = discord.ui.TextInput(label="Podaj kwotę w PLN", placeholder="Np. 100")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            kwota = float(self.kwota.value)
        except:
            return await interaction.response.send_message("❌ Podaj poprawną liczbę.", ephemeral=True)

        await interaction.response.send_message(
            "Wybierz metodę płatności:",
            view=MetodaView(kwota, "otrzymam"),
            ephemeral=True
        )


# ===== MODAL 2 =====
class IleMuszeDacModal(discord.ui.Modal, title="Ile muszę dać?"):
    dolarki = discord.ui.TextInput(label="Ile chcesz dostać $?", placeholder="Np. 500000")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            dolarki = float(self.dolarki.value)
        except:
            return await interaction.response.send_message("❌ Podaj poprawną liczbę.", ephemeral=True)

        await interaction.response.send_message(
            "Wybierz metodę płatności:",
            view=MetodaView(dolarki, "dac"),
            ephemeral=True
        )


# ===== SELECT MENU =====
class MetodaView(discord.ui.View):
    def __init__(self, wartosc, tryb):
        super().__init__(timeout=60)
        self.add_item(MetodaSelect(wartosc, tryb))


class MetodaSelect(discord.ui.Select):
    def __init__(self, wartosc, tryb):
        options = [
            discord.SelectOption(label=nazwa)
            for nazwa in METODY.keys()
        ]

        super().__init__(
            placeholder="Wybierz metodę płatności",
            options=options
        )

        self.wartosc = wartosc
        self.tryb = tryb

    async def callback(self, interaction: discord.Interaction):
        metoda = self.values[0]
        procent = METODY[metoda]

        embed = discord.Embed(
            title="💰 WYNIK",
            color=0x2f3136
        )

        if self.tryb == "otrzymam":
            kwota = self.wartosc
            prowizja = max(kwota * procent, MIN_PROWIZJA)
            netto = kwota - prowizja

            kurs = pobierz_kurs(kwota)
            dolarki = int(netto * kurs)

            embed.add_field(name="Metoda", value=metoda, inline=False)
            embed.add_field(name="Kwota", value=f"{kwota:.2f} zł", inline=False)
            embed.add_field(name="Prowizja", value=f"{prowizja:.2f} zł", inline=False)
            embed.add_field(name="Otrzymasz", value=f"{dolarki:,} $", inline=False)

        else:
            dolarki = self.wartosc
            kurs = 4500
            kwota_netto = dolarki / kurs

            prowizja = max(kwota_netto * procent, MIN_PROWIZJA)
            kwota_brutto = kwota_netto + prowizja

            embed.add_field(name="Metoda", value=metoda, inline=False)
            embed.add_field(name="Musisz zapłacić", value=f"{kwota_brutto:.2f} zł", inline=False)

        await interaction.response.edit_message(content=None, embed=embed, view=None)


# ===== KOMENDA DO WYSŁANIA PANELU =====
@bot.command()
@commands.has_permissions(administrator=True)
async def panel(ctx):
    embed = discord.Embed(
        title="📦 TOXICSHOP × KALKULATOR",
        description="Aby w szybki i prosty sposób obliczyć:\n"
                    "• ile otrzymasz waluty za określoną ilość PLN\n"
                    "• ile musisz dać PLN, aby otrzymać określoną ilość waluty\n\n"
                    "Kliknij przycisk poniżej.",
        color=0x2f3136
    )

    await ctx.send(embed=embed, view=KalkulatorView())


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")


bot.run(TOKEN)
