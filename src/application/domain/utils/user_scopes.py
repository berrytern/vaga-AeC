from enum import Enum


class UserScopes(Enum):
    ADMIN = [
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
        "bkf:c",
        "bkf:r",
        "bkf:d",  # Favorite
    ]
    READER = [
        "rd:r",
        "rd:u",
        "rd:d",  # Reader
        "bkf:c",
        "bkf:r",
        "bkf:d",  # Favorite
    ]
