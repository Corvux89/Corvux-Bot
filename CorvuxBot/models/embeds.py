from typing import Dict

import discord.utils
from discord import Embed, Color, Member

from CorvuxBot.helpers import split_dict
from CorvuxBot.models.characters import Character


class ErrorEmbed(Embed):
    def __init__(self, **kwargs):
        kwargs['title'] = "Error:"
        kwargs['color'] = Color.brand_red()
        super().__init__(**kwargs)


def GetEmbed(character: Character, player: Member) -> Embed:
    description = f'**Class:** {character.character_class}\n' \
                  f'**Level:** {character.level}\n'

    embed = Embed(title=f'Character Info - {character.name}',
                  description=description,
                  color=Color.dark_grey())

    embed.set_thumbnail(url=player.display_avatar.url)
    return embed


class dashboard_embed(Embed):
    def __init__(self, channel_statuses: Dict[str, str], category_name: str):
        super(dashboard_embed, self).__init__(color=Color.dark_grey(),
                                              title=f'Channel Statuses - {category_name}',
                                              description="<:white_check_mark:983576747381518396> = Channel available\n"
                                                          "<:x:983576786447245312> = Channel in use\n"
                                                          "<:bookmark:986735232604598302> = Waiting for Magewright\n"
                                                          "<:grey_question:983576825294884924> = Unknown. Check the channel for more details",
                                              timestamp=discord.utils.utcnow())

        #TODO: Split channel_statuses into chunks of 20 to handle large categories

        # vals = dict()
        # for test in split_dict(channel_statuses,20):
        #     vals.add(test)

        channels = ""
        statuses = ""

        for k in channel_statuses.keys():
            channels += f'{k}\n'
            statuses += f'\u200B \u200B \u200B \u200B \u200B {channel_statuses[k]}\n'

        self.add_field(name="Channel", value=channels, inline=True)
        self.add_field(name="Available", value=statuses, inline=True)

        if secondary_statuses is not None:
            self.add_field(name="\u200B", value="\u200b", inline=False)
            channels = ""
            statuses = ""

            for k in secondary_statuses.keys():
                channels += f'{k}\n'
                statuses += f'\u200B \u200B \u200B \u200B \u200B {secondary_statuses[k]}\n'

            self.add_field(name="Channel", value=channels, inline=True)
            self.add_field(name="Available", value=statuses, inline=True)

        self.set_footer(text="Last Updated")
