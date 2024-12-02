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
        "rd:d",  # Reader
        "bk:c",
        "bk:ra",
        "bk:r",
        "bk:u",
        "bk:d",  # Book
    ]
    READER: List[str] = [
        "rd:r",
        "rd:u",
        "rd:d",  # Reader
    ]
