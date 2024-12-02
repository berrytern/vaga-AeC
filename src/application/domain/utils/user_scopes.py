from typing import List
from enum import Enum


class UserScopes(Enum):
    ADMIN: List[str] = [
        "ad:c",
        "ad:ra",
        "ad:r",
        "ad:u",
        "cl:c",
        "cl:ra",
        "cl:r",
        "cl:u",
        "cl:d",  # Admin
    ]
    CLIENT: List[str] = []  # Client
