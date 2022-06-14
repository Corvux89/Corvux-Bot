from CorvuxBot.sheets_client import GSheetsClient
from CorvuxBot.category_ref import CharacterClass
from time import perf_counter
from typing import Optional, Dict, Any


class Character(object):
    player_id: int
    name: str
    _character_class: CharacterClass
    level: int

    def __init__(self,
                 player_id: int,
                 name: str,
                 char_class: CharacterClass,
                 level: int):
        self.player_id = player_id
        self.name = name
        self._character_class = char_class
        self.level = level

    @classmethod
    def from_dict(cls,
                  char_dict: Dict[str, Any]):
        character = cls(player_id=int(char_dict["Member ID"]),
                        name=char_dict["Name"],
                        char_class=CharacterClass(char_dict["Class"]),
                        level=char_dict["Level"])
        return character

    @property
    def character_class(self) -> str:
        return self._character_class.value


class characters(GSheetsClient):
    sheets: GSheetsClient

    def __init__(self):
        super(characters, self).__init__()
        self.sheets = GSheetsClient

        start = perf_counter()
        self.char_sheet = self.corvux_workbook.worksheet("Characters")
        end = perf_counter()
        print(f'Time to load character sheet: {end - start}s')

    def get_character_from_id(self, member_id: int | str) -> Optional[Character]:
        if isinstance(member_id, int):
            member_id = str(member_id)

        header_row = '1:1'
        target_cell = self.char_sheet.find(member_id, in_column=1)
        if not target_cell:
            return None

        user_row = str(target_cell.row) + ":" + str(target_cell.row)
        data = self.char_sheet.batch_get([header_row,user_row])
        data_dict = {k: v for k, v in zip(data[0][0], data[1][0])}

        return Character.from_dict(data_dict)

    def create_character(self, character: Character):
        character_data = [
            str(character.player_id),
            character.name,
            character.character_class,
            character.level
        ]

        print(f'Appending new character to sheet with data {character_data}')
        self.char_sheet.append_row(character_data,
                                   value_input_option='USER_ENTERED',
                                   insert_data_option="INSERT_ROWS",
                                   table_range='A2')