import logging
from typing import Dict
import discord.utils
from discord import Embed, Color, Member
from CorvuxBot.constants import *
from CorvuxBot.models.characters import Character

log = logging.getLogger(__name__)


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
                                              description=f"{WHITE_CHECK} = Channel available\n"
                                                          f"{RED_X} = Channel in use\n"
                                                          f"{BOOKMARK} = Waiting for Magewright\n"
                                                          f"{GREY_QUESTION} = Unknown. Check the channel for more details",
                                              timestamp=discord.utils.utcnow())

        # TODO: Can we optimize this for mobile to get around discord bug?
        channels = ""
        statuses = ""
        counter = 0
        maxUpdates = len(channel_statuses)

        for k in channel_statuses.keys():
            counter += 1
            channels += f'{k}\n'
            statuses += f'\u200B \u200B \u200B \u200B \u200B {channel_statuses[k]}\n'

            if CHUNKS >= maxUpdates == counter:
                self.add_field(name="Channel", value=channels, inline=True)
                self.add_field(name="Available", value=statuses, inline=True)
            elif counter % CHUNKS == 0:
                self.add_field(name="Channel", value=channels, inline=True)
                self.add_field(name="Available", value=statuses, inline=True)
                channels = ""
                statuses = ""
                maxUpdates -= CHUNKS
                counter -= CHUNKS
                self.add_field(name="\u200B", value="\u200b", inline=False)

        self.set_footer(text="Last Updated")
