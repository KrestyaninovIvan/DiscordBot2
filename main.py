import discord

from discord import app_commands
from base import WorkBase


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1023151612644036638))
        print('Online')


client = MyClient()
tree = app_commands.CommandTree(client)
base = WorkBase('BOT.db')


@tree.command(name="tap", description="tap tap", guild=discord.Object(id=1023151612644036638))
async def self(interaction: discord.Interaction):
    base.check_base_start()
    await interaction.response.send_message('Да-да?', ephemeral=True)


client.run('MTAyMzE1Mjc5ODY2NzM5MDk5Ng.Gdxtmp.t2LRkpjCBI-3UmB-jgx3tL4xUZPWy7B9TvjM-8')
