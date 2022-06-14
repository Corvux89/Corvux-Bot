import discord
from typing import Dict, Any
from discord import Embed, Color, Member

from CorvuxBot.models.characters import Character


def linebreak() -> Dict[str, Any]:
    return {
        'name': discord.utils.escape_markdown('___________________________________________'),
        'value': '\u200B',
        'inline': False
    }


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
                  color = Color.dark_grey())

    embed.set_thumbnail(url=player.display_avatar.url)
    return embed
