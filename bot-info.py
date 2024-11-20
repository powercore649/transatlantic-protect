import discord
from discord.ext import commands
from discord import app_commands
import time

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()  # Initialisation du temps de démarrage

    @app_commands.command(name="botinfo", description="Affiche des informations sur le bot.")
    async def botinfo(self, interaction: discord.Interaction):
        # Calcul de l'uptime local
        uptime_seconds = int(time.time() - self.start_time)
        uptime_hours, remainder = divmod(uptime_seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(remainder, 60)
        uptime = f"{uptime_hours} heures, {uptime_minutes} minutes et {uptime_seconds} secondes"

        # Création du bot
        bot_creation_timestamp = (self.bot.user.id >> 22) + 1420070400000
        bot_creation_date = f"<t:{bot_creation_timestamp // 1000}:F>"

        # Récupérer l'ID du propriétaire du bot
        owner = self.bot.get_user(self.bot.owner_id)
        owner_name = owner.name if owner else "networker_project2024"  # Si le propriétaire est inconnu (par exemple, si le bot n'est pas sur un serveur)

        embed = discord.Embed(
            title="🤖 · Informations sur le BOT :",
            description=f"""
👑 **Mon créateur** : `{owner_name}#{self.bot.owner_id}`

📆 **Création** : {bot_creation_date}

🔋 **Uptime local** : {uptime}

🔗 **Liens utiles** :
- [Ajouter le bot](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands)
- [Support](https://discord.gg/nqQPagSfvb)
- [PayPal](https://paypal.me/aurorascom?country.x=CA&locale.x=fr_CA)
- [Site web](https://circlentreprise1.vercel.app/)

📊 **Statistiques** :
- **Serveurs** : `{len(self.bot.guilds)}`
- **Utilisateurs** : `{sum(guild.member_count for guild in self.bot.guilds if guild.member_count)}`

✅ **Ping** : `{round(self.bot.latency * 1000)} ms`
            """,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else "")
        embed.set_footer(text=f"Commande utilisée par {interaction.user.name}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
