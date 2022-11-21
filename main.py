from typing import List
import json
import discord
import string
import atexit

from discord import app_commands
from discord.ext import commands
from base import WorkBase
from discordembed import DiscordEmbed
from timeconversion import SecondsConvert


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), )

    async def on_ready(self):
        await tree.sync(guild=guild)
        print('Online')


client = MyClient()
tree = app_commands.CommandTree(client)
base = WorkBase('BOT.db')
embed = DiscordEmbed()
guild = discord.Object(id=218853609352331264)
sc = SecondsConvert()


@tree.command(name="пользователи", description="вывод топ по времени в игре", guild=guild)
async def top(interaction: discord.Interaction, day: int = None):
    if day is None:
        userstime = base.user_time(interaction.guild.name.replace(" ", "") + 'Game')
    else:
        period = SecondsConvert(day)
        userstime = base.user_time_period(interaction.guild.name.replace(" ", "") + 'Game', period.date)
    description = embed.description_emdeb(userstime, 'За все время', day, client)
    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
    footer_text = embed.footer_emdeb(userstime)
    newembed = embed.tree_embed(description, url, footer_text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)


@tree.command(name="статистика", description="вывод игр по времени", guild=guild)
async def statistics(interaction: discord.Interaction, day: int = None):
    if day is None:
        timegame = base.game_time(interaction.guild.name.replace(" ", "") + 'Game')
    else:
        period = SecondsConvert(day)
        timegame = base.game_time_period(interaction.guild.name.replace(" ", "") + 'Game', period.date)
    description = embed.description_emdeb(timegame, 'За все время', day)
    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
    footer_text = embed.footer_emdeb(timegame)
    newembed = embed.tree_embed(description, url, footer_text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)


@tree.command(name="статпользовател", description="вывод игр пользователя по времени", guild=guild)
async def statistics_member(interaction: discord.Interaction, member: discord.Member, day: int = None):
    if day is None:
        gameuser = base.game_time_id(interaction.guild.name.replace(" ", "") + 'Game', member.id)
    else:
        period = SecondsConvert(day)
        gameuser = base.game_time_id_period(interaction.guild.name.replace(" ", "") + 'Game', member.id, period.date)
    description = embed.description_emdeb(gameuser, f'Пользователь **{member.name}** ', day)
    url = member.display_avatar
    footer_text = embed.footer_emdeb(gameuser)
    newembed = embed.tree_embed(description, url, footer_text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)


@tree.command(name='я', description="вывод игр пользователя по времени", guild=guild)
async def statistics_me(interaction: discord.Interaction, day: int = None):
    member = interaction.user
    if day is None:
        gameuser = base.game_time_id(interaction.guild.name.replace(" ", "") + 'Game', member.id)
    else:
        period = SecondsConvert(day)
        gameuser = base.game_time_id_period(interaction.guild.name.replace(" ", "") + 'Game', member.id, period.date)
    description = embed.description_emdeb(gameuser, f'Пользователь **{member.name}** ', day)
    url = member.display_avatar
    footer_text = embed.footer_emdeb(gameuser)
    newembed = embed.tree_embed(description, url, footer_text)
    await interaction.response.send_message('Да-да?', ephemeral=True, embed=newembed)


@client.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.content.split(' ')}.intersection(json.load(open('words.json'))) != set():
        name = message.guild.name.replace(" ", "")
        base.base_update(name, message.author.id)

    await client.bot.process_commands(message)
    if message.author.id == 219779423904202752:  # Димин id
        if 'https://' in message.content or message.content == '':
            description = "«Oh My God! Who the hell cares?!»\n© (Peter Griffin)"
            url = 'https://s00.yaplakal.com/pics/pics_original/7/4/0/15640047.jpg'
            embed = discord.Embed(description=description, color=0xFF0000)
            embed.set_thumbnail(url=url)
            await client.get_channel(message.channel.id).send(embed=embed)


@client.event
async def on_ready():
    for guild in client.guilds:
        base.create_base(guild.name.replace(" ", ""))
    print('Online')
    sc = SecondsConvert()
    tables = base.fetchall
    for table in tables:
        for guild in client.guilds:
            if table[1] == guild.name.replace(" ", "") + 'Game':
                if sc.day == 1:
                    top_game = base.execute_top_3(True, table[1], sc.months_minus, sc.date)
                    category = guild.categories[0]
                    channel = category.channels[0]
                    description = embed.description_emdeb(top_game, f'Топ игр c', 30)
                    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
                    footer_text = embed.footer_emdeb(top_game)
                    newembed = embed.tree_embed(description, url, footer_text)
                    await client.get_channel(channel.id).send(embed=newembed)

                    top_game = base.execute_top_3(False, table[1], sc.months_minus, sc.date)
                    description = embed.description_emdeb(top_game, f'Топ игроков', 30, client)
                    url = 'https://images.fineartamerica.com/images/artistlogos/2-kate-green-1479756827-square.jpg'
                    footer_text = embed.footer_emdeb(top_game)
                    newembed = embed.tree_embed(description, url, footer_text)
                    await client.get_channel(channel.id).send(embed=newembed)

@client.event
async def on_member_join(member):
    await member.send('Я за тобой слежу и кстати информация по командам череp !инфо')
    for ch in client.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await client.get_channel(ch.id).send(f'{member}, смотрите кто теперь в нашей гачи тусовке')


@client.event
async def on_member_remove(member):
    for ch in client.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await client.get_channel(ch.id).send(f'{member}, теперь будет гачиться в другом месте')


@client.event
async def on_presence_update(before, after):
    if before.activity is not None:
        activity_type = str(before.activity.type)
        if activity_type == 'ActivityType.playing':
            name = before.guild.name.replace(" ", "") + 'Game'
            game = before.activity.name
            time_start = before.activity.start.replace(tzinfo=None)
            user_id = before.id
            time_end = SecondsConvert()
            game_time = time_end.time_to_second(time_start)
            base.database_repetition(name, user_id, game, time_start, game_time)


def goodbye():
    for member in client.get_all_members():
        if member.activity is not None:
            name = member.guild.name.replace(" ", "") + 'Game'
            game = member.activity.name
            time_start = member.activity.start.replace(tzinfo=None)
            user_id = member.id
            time_end = SecondsConvert()
            game_time = time_end.time_to_second(time_start)
            base.database_repetition(name, user_id, game, time_start, game_time)


atexit.register(goodbye)

client.run('MTAyNDI5MTM1MTQ3MjM3Mzc5MA.G2Ys7n.EE4MC6icDLNvjrixhicFxVJsPXkhRQ5XSkTDv8')
