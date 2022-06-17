import enum
from typing import List
from discord import OptionChoice


class CommandOptionEnum(enum.Enum):

    @classmethod
    def optionchoice_list(cls) -> List[OptionChoice]:
        return list(map(lambda o: OptionChoice(o.value), cls))

    @classmethod
    def values_list(cls) -> List[str]:
        return list(map(lambda v: v.value, cls))


class CharacterClass(CommandOptionEnum):
    ARTIFICER = 'Artificer'
    BARBARIAN = 'Barbarian'
    BARD = 'Bard'
    CLERIC = 'Cleric'
    DRUID = 'Druid'
    FIGHTER = 'Fighter'
    MONK = 'Monk'
    PALADIN = 'Paladin'
    RANGER = 'Ranger'
    ROGUE = 'Rogue'
    SORCERER = 'Sorcerer'
    WARLOCK = 'Warlock'
    WIZARD = 'Wizard'
