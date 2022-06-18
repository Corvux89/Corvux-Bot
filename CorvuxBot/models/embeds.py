import logging
from collections import defaultdict
import discord.utils
from discord import Embed, Color, Member
from CorvuxBot.constants import *
from CorvuxBot.models.characters import PlayerCharacter

log = logging.getLogger(__name__)


class ErrorEmbed(Embed):
    def __init__(self, **kwargs):
        kwargs['title'] = "Error:"
        kwargs['color'] = Color.brand_red()
        super().__init__(**kwargs)


def GetEmbed(character: PlayerCharacter, player: Member) -> Embed:
    description = f'**Class:** {character.character_class}\n' \
                  f'**Level:** {character.level}\n'

    embed = Embed(title=f'Character Info - {character.name}',
                  description=description,
                  color=Color.dark_grey())

    embed.set_thumbnail(url=player.display_avatar.url)
    return embed


class dashboard_embed(Embed):
    def __init__(self, channel_statuses: defaultdict(list), category_name: str):
        super(dashboard_embed, self).__init__(color=Color.dark_grey(),
                                              title=f'Channel Statuses - {category_name}',
                                              timestamp=discord.utils.utcnow())

        for k, v in channel_statuses.items():
            counter = 0
            channels = ""
            if isinstance(v, list):
                if len(v) == 0:
                    channels += "None"
                else:
                    for c in v:
                        counter += 1
                        channels += f"\n{c}"

            self.add_field(name=k,
                           value=channels,
                           inline=True)
            self.add_field(name="\u200B", value="\u200b", inline=False)

        self.set_footer(text="Last Updated")
