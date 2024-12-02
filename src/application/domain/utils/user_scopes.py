from typing import List
from enum import Enum


class UserScopes(Enum):
    ADMIN: List[str] = [
        "ad:c",
        "ad:ra",
        "ad:r",
        "ad:u",  # Admin
        "rd:c",
        "rd:ra",
        "rd:r",
        "rd:u",
        "rd:d",
    ]
    READER: List[str] = [
        "rd:ra",
        "rd:r",
        "rd:u",
        "rd:d",
    ]  # Reader
