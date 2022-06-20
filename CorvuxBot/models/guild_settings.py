from typing import Optional, List

DEFAULT_MAGEWRIGHT_ROLE_NAMES = {"magewright"}

class ServerSettings(object):
    guild_id: int
    admin_roles: Optional[List[int]] = None

