import inspect
import logging
import traceback
from typing import List, Optional

from CorvuxBot.models.characters import PlayerCharacter

log = logging.getLogger(__name__)

def get_character_from_id(self, member_id: int | str) -> Optional[PlayerCharacter]:
    if isinstance(member_id, int):
        member_id = str(member_id)

    header_row = '1:1'
    target_cell = self.sheet.char_sheet.find(member_id, in_column=1)
    if not target_cell:
        return None

    user_row = str(target_cell.row) + ":" + str(target_cell.row)
    data = self.sheet.char_sheet.batch_get([header_row, user_row])
    data_dict = {k: v for k, v in zip(data[0][0], data[1][0])}

    return PlayerCharacter.from_dict(data_dict)


def create_character(self, character: PlayerCharacter):
    character_data = [
        str(character.player_id),
        character.name,
        character.character_class,
        character.level
    ]

    log.info(f'Appending new character to sheet with data {character_data}')
    self.sheet.char_sheet.append_row(character_data,
                                     value_input_option='USER_ENTERED',
                                     insert_data_option="INSERT_ROWS",
                                     table_range='A2')
