import discord
from timeconversion import DataOut


class DiscordEmbed:

    def __init__(self):
        self.__iconurl = 'https://cdn.onlinewebfonts.com/svg/download_378989.png'

    def tree_embed(self, description, url, footertext, iconurl=None, color=None):
        if iconurl is None:
            iconurl = self.__iconurl
        embed = discord.Embed(description=description, color=color)
        embed.set_thumbnail(url=url)
        embed.set_footer(text=footertext, icon_url=iconurl)
        return embed

    def description_emdeb(self, top_game, description, day, client=None):
        tg = DataOut()
        if day is None or day == 0:
            description += f'\n'
        else:
            description += f'за период {day} дней'
        for i in top_game:
            tg.time_update(i[1])
            if client:
                description += f'\t{client.get_user(i[0]).display_name} - '
            elif client is None:
                description += f'\t{i[0]} - '
            description += f'{tg.output_days(True)}, '
            description += f'{tg.output_hours(True)}, '
            description += f'{tg.output_minutes(True)}\n'
        return description
