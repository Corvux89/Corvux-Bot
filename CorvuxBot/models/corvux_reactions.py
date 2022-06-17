import logging
from time import perf_counter
from typing import List

from discord import TextChannel

from CorvuxBot.sheets_client import GSheetsClient

log = logging.getLogger(__name__)


class CorvuxReaction(object):
    channel_id: int
    post_id: int
    emote: str
    role_id: int

    def __init___(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls,
                  reaction_dict: Dict[str, Any]):
        reaction = cls(channel_id = int(reaction_dict["channel_id"]),
                       post_id = int(reaction_dict["post_id"]),
                       emote = str(reaction_dict["emote"]),
                       role_id = int(reaction_dict["role_id"]))
        return reaction


class reactions(GSheetsClient):

    def __init__(self):
        super(reactions,self).__init__()

        start = perf_counter()
        self.reactions_sheet = self.corvux_workbook.worksheet("Reactions and Roles")
        end = perf_counter()
        log.info(f'Time to load dashboard sheet: {end - start}s')

    def get_role_by_post_id(self, post_id: int) -> Optional[CorvuxReaction]:
        if isinstance(post_id, int):
            post_id = str(post_id)

        header_row = '1:1'
        target_cell = self.reactions_sheet.find(post_id, in_column=2)
        if not target_cell:
            return None

    def get_channels(self) -> List[TextChannel]:
        vals = self.reactions_sheet.col_values(1)
        return vals