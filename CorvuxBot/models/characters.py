import logging
from CorvuxBot.category_ref import CharacterClass
from typing import Dict, Any

log = logging.getLogger(__name__)


class PlayerCharacter(object):
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
