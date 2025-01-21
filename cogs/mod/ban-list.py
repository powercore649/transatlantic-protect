import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import asyncio

class BanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban-list", description="Affiche la liste des utilisateurs bannis du serveur")
    async def ban_list(self, interaction: discord.Interaction):
        # Vérifier les permissions de l'utilisateur
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message(
                "🚫 Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True
            )

        # Collecter les utilisateurs bannis
        bans = [ban async for ban in interaction.guild.bans()]  # Utilisation d'une compréhension asynchrone
        if not bans:
            return await interaction.response.send_message(
                embed=discord.Embed(title="Aucun utilisateur banni.", color=discord.Color.red()), ephemeral=True
            )

        # Pagination
        per_page = 10
        total_bans = len(bans)
        pages = (total_bans + per_page - 1) // per_page
        current_page = 0

        def get_embed(page):
            start = page * per_page
            end = start + per_page
            description = "\n".join(
                [f"{i + 1}) {ban_entry.user} ({ban_entry.user.id})" for i, ban_entry in enumerate(bans[start:end], start=start)]
            )
            embed = discord.Embed(
                title="Liste des utilisateurs bannis",
                description=description,
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Page {page + 1}/{pages} • Total : {total_bans}")
            return embed

        embed = get_embed(current_page)

        # Boutons de navigation
        prev_button = Button(label="◀", style=discord.ButtonStyle.grey)
        next_button = Button(label="▶", style=discord.ButtonStyle.grey)
        view = View()

        async def update_buttons():
            prev_button.disabled = current_page == 0
            next_button.disabled = current_page == pages - 1

        async def prev_callback(interaction: discord.Interaction):
            nonlocal current_page
            current_page -= 1
            await update_buttons()
            await interaction.response.edit_message(embed=get_embed(current_page), view=view)

        async def next_callback(interaction: discord.Interaction):
            nonlocal current_page
            current_page += 1
            await update_buttons()
            await interaction.response.edit_message(embed=get_embed(current_page), view=view)

        prev_button.callback = prev_callback
        next_button.callback = next_callback

        await update_buttons()
        view.add_item(prev_button)
        view.add_item(next_button)

        # Envoyer le message initial
        await interaction.response.send_message(embed=embed, view=view)

        # Supprimer les boutons après 5 minutes
        await asyncio.sleep(300)
        await interaction.edit_original_response(view=None)

async def setup(bot: commands.Bot):
    await bot.add_cog(BanList(bot))
