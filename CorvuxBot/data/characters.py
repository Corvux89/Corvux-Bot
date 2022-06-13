import discord
from CorvuxBot.sheets_client import GSheetsClient
from CorvuxBot.data.category_ref import CharacterClass
from time import perf_counter
from discord.commands.context import ApplicationContext
from typing import Optional, Dict, Any
from gspread import Cell
from discord import Member


class Character(object):
    player_id: int
    name: str
    level: int
    _character_class: CharacterClass


    def __init__(self, player_id: int, name: str, char_class: CharacterClass):
        self.player_id = player_id
        self.name = name
        self._character_class = char_class

    @classmethod
    def from_dict(cls, char_dict: Dict[str, Any]):
        character = cls(player_id=int(char_dict["Discord ID"]),
                        name=char_dict["Name"],
                        level=int(char_dict["Level"]),
                        char_class=CharacterClass(char_dict["Class"]))
        return character

    @property
    def level(self):
        return self.level.value

    def get_member(self, ctx: ApplicationContext) -> discord.Member:
        return discord.utils.get(ctx.guild.members, id=self.player_id)

class characters(object):
    sheets: GSheetsClient
    def __init__(self):
        self.sheets = GSheetsClient()

        #Worksheet
        start = perf_counter()
        self.char_sheet = self.sheets.corvux_workbook.worksheet('Characters')
        end = perf_counter()
        print(f'Time to load character sheet {start-end}s')

    def create_character(self, character: Character):
        character_data = [
            str(character.player_id),
            character.name,
            character._character_class
        ]
        print(f'Appending new character to sheet with data {character_data}')

        self.char_sheet.append_row(character_data,
                                   value_input_option='USER_ENTERED',
                                   insert_data_option='INSERT_ROWS',
                                   table_range='A2')

    def get_character_from_id(self, discord_id: int | str) -> Optional[Character]:
        if isinstance(discord_id, int):
            discord_id = str(discord_id)
        header_row = '1:1'
        target_cell = self.char_sheet.find(discord_id, in_column=1)
        if not target_cell:
            return None

        user_row = str(target_cell.row) + ':' + str(target_cell.row)
        data = self.char_sheet.bath_get([header_row, user_row])
        data_dict = {k: v for k, v in zip(data[0][0], data[1][0])}

        return Character.from_dict(data_dict)