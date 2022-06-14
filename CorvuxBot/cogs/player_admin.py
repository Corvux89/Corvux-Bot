import discord
import time
from discord import ApplicationContext, Option, Member, Embed
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import *
from discord.ext import commands
from CorvuxBot.models.embeds import ErrorEmbed, GetEmbed
from CorvuxBot.models.characters import Character
from CorvuxBot.category_ref import CharacterClass


def setup(bot):
    bot.add_cog(PlayerAdmin(bot))


class PlayerAdmin(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        print(f'Cog \'Player_Admin\' loaded')

    @staticmethod
    async def cog_before_invoke(ctx: Context):
        await cog_log(ctx)

    @commands.slash_command(name="create",
                            description="Create a new character")
    async def create_character(self,
                               ctx: ApplicationContext,
                               player: Option(Member,
                                              "Character's Player",
                                              required=True),
                               name: Option(str,
                                            "Character's name",
                                            required=True),
                               character_class: Option(str,
                                                       "Character's class",
                                                       choices=CharacterClass.optionchoice_list(),
                                                       required=True),
                               level: Option(int,
                                             "Starting level for higher-level characters",
                                             min_value=1,
                                             max_value=20,
                                             default=1)
                               ):
        start = time.time()

        await ctx.response.defer(ephemeral=True)

        if self.bot.characters.get_character_from_id(player.id) is not None:
            print(f'Found existing character for {player.id}. Aborting.')
            await ctx.respond(embed=ErrorEmbed(description=f'Player {player.mention} already has a character. Do something else.'),
                              ephemeral=True)
            return
        else:
            new_character = Character(player.id,
                                      name,
                                      CharacterClass(character_class),
                                      level)
            self.bot.characters.create_character(new_character)

            embed = Embed(title=f'Character Created - {name}',
                          description=f'**Player:** {player.mention}\n'
                                      f'**Class:** {character_class}\n'
                                      f'**Starting Level:** {level}',
                          color=discord.Color.random())

            embed.set_thumbnail(url=player.display_avatar.url)
            embed.set_footer(text=f'Created by: {ctx.author.name}#{ctx.author.discriminator}',
                             icon_url=ctx.author.display_avatar.url)

            await ctx.respond(embed=embed)
            end = time.time()
            print(f'Time to create character: {end - start}s')

    @commands.slash_command(name="get",
                            description="Gets a characters information")
    async def getCharacter(self,
                           ctx: ApplicationContext,
                           player: Option(Member,
                                          "Player to get the information of",
                                          required=False,)):

        if player is None:
            player = ctx.author

        await ctx.response.defer()

        if (character := self.bot.characters.get_character_from_id(player.id)) is None:
            print(f'No character information found for player [ {player.id} ]. Aborting.')
            await ctx.respond(embed=ErrorEmbed(description=f'No character information found for {player.mention}'),
                              ephemeral=True)
            return
        else:
            await ctx.respond(embed=GetEmbed(character,player), ephemeral=False)