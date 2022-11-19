from typing import List

import discord

from discord import app_commands
from base import WorkBase
from discordembed import DiscordEmbed
from timeconversion import SecondsConvert

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        await tree.sync(guild=guild)
        print('Online')


client = MyClient()
tree = app_commands.CommandTree(client)
base = WorkBase('BOT.db')
embed = DiscordEmbed()
guild = discord.Object(id=1023151612644036638)
sc = SecondsConvert()

@tree.command(name="топ", description="вывод топ по времени в игре", guild=guild)
async def top(interaction: discord.Interaction):
    userstime = base.users_sum_time(interaction.guild.name.replace(" ", "") + 'Game')
    description = embed.description_emdeb(userstime, 'За все время', None, client)
    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
    text = 'Это футер'
    newembed = embed.tree_embed(description, url, text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)

@tree.command(name="статистика", description="вывод игр по времени", guild=guild)
async def statistics(interaction: discord.Interaction):
    timegame = base.games_sum_time(interaction.guild.name.replace(" ", "") + 'Game')
    description = embed.description_emdeb(timegame, 'За все время', None)
    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
    text = 'Это футер'
    newembed = embed.tree_embed(description, url, text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)

@tree.command(name="статпользовател", description="вывод игр пользователя по времени", guild=guild)
async def statistics_member(interaction: discord.Interaction, member: discord.Member, day: int = None):
    if day is None:
        gameuser = base.games_user(interaction.guild.name.replace(" ", "") + 'Game', member.id)
    else:
        period = SecondsConvert(day)
        gameuser = base.games_time_user(interaction.guild.name.replace(" ", "") + 'Game', member.id, period.date)
    description = embed.description_emdeb(gameuser, f'Пользователь **{member.name}** ', day)
    url = member.display_avatar
    text = 'Это футер'
    newembed = embed.tree_embed(description, url, text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)

   # await interaction.response.send_message(f'Your favourite fruit seems to be {period}')



client.run('MTAyMzE1Mjc5ODY2NzM5MDk5Ng.Gdxtmp.t2LRkpjCBI-3UmB-jgx3tL4xUZPWy7B9TvjM-8')
