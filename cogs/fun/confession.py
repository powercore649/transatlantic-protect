import discord
from discord import app_commands
from discord.ext import commands

class Confession(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.confession_channel = None  # Remplacer par le salon où les confessions doivent être envoyées
    
    @app_commands.command(name="confession", description="Send an anonymous confession.")
    @app_commands.describe(confession="Your anonymous confession", image="An optional image to accompany your confession")
    async def confession(self, interaction: discord.Interaction, confession: str, image: discord.Attachment = None):
        if not confession:
            await interaction.response.send_message("You need to write something to confess!", ephemeral=True)
            return
        
        # Si le salon de confession est défini
        if self.confession_channel:
            embed = discord.Embed(
                title="Anonymous Confession",
                description=confession,
                color=0x00FF00
            )
            embed.set_footer(text="All confessions are anonymous, the name of the person will never be displayed.")

            # Si une image est jointe
            if image:
                embed.set_image(url=image.url)

            # Envoi du message dans le salon de confession
            await self.confession_channel.send(embed=embed)

            # Informer l'utilisateur que sa confession a été envoyée
            await interaction.response.send_message("Your confession has been sent anonymously.", ephemeral=True)
        else:
            await interaction.response.send_message("Confessions are not set up yet. Please contact the admin.", ephemeral=True)
    
    @app_commands.command(name="set_confession_channel", description="Set the confession channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_confession_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the channel where the confessions will be sent."""
        self.confession_channel = channel
        await interaction.response.send_message(f"Confession channel has been set to {channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Confession system is online!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Confession(bot))
