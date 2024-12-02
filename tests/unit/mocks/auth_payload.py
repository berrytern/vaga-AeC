from uuid import uuid4
from datetime import datetime, timedelta

EXP_TIME_IN_SECONDS = 10000

ADMIN_SCOPE = ["ad:c", "ad:r", "ad:u", "ad:d"]

ADMIN_PAYLOAD = {
    "sub": f"{uuid4()}",
    "iss": "berrytern",
    "type": "admin",
    "iat": datetime.utcnow(),
    "scope": ADMIN_SCOPE,
    "exp": datetime.utcnow() + timedelta(seconds=EXP_TIME_IN_SECONDS),
}

EXP_TIME_IN_SECONDS = 10000

READER_SCOPE = ["rd:c", "rd:r", "rd:u", "rd:d"]

READER_PAYLOAD = {
    "sub": f"{uuid4()}",
    "iss": "berrytern",
    "type": "reader",
    "iat": datetime.utcnow(),
    "scope": READER_SCOPE,
    "exp": datetime.utcnow() + timedelta(seconds=EXP_TIME_IN_SECONDS),
}
