from typing import Optional, cast
from contextvars import ContextVar
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_session


# Token expiration time in seconds
TOKEN_EXP_TIME = 5 * 60 * 60
REFRESH_TOKEN_EXP_TIME = 24 * 60 * 60
# Prefix for reset password key in Redis
RESET_PASSWD_PREFIX = "reset_passwd_"


RESET_PASSWD_SUBJECT = "Request to reset your password account login password"
RESET_PASSWD_BODY_TEXT = """Dear {name},
We have received a request to reset the password for your account. If this request came from you,
please click <a href="{link}">here</a> within the next {exp_time} minutes to complete the password reset.
If you have not asked for a password reset, please ignore this e-mail.

Should you have any questions, always feel free to contact our support team: <a href="mailto:{support_email}?
subject=Support Me to Recover Access to My Account&body=Hi, I am failling to recover my password. Please, Help me!
</a>.

Best regards,

Support team
"""
RESET_PASSWD_BODY_HTML = """\
<html>
    <head></head>
    <body>
        <p>
            Dear {name},
            <br/><br/>
            We have received a request to reset the password for your account. If this request came from you,
            please click <a href="{link}">here</a> within the next {exp_time} minutes to complete the password reset.
            <br/><b>If you have not asked for a password reset, please ignore this e-mail.</b>
            <br/><br/>
            Should you have any questions, always feel free to contact our
             <a href="mailto:{support_email}?subject=Support Me to Recover Access to My Account&body=Hi, I am failling to recover my password. Please, Help me!">support team</a>.
            <br/><br/>
            Best regards,
            <br/><br/>
            Support team
        </p>
    </body>
</html>
"""  # noqa: E501


db_session_var: ContextVar[Optional[AsyncSession]] = cast(
    ContextVar[Optional[AsyncSession]], ContextVar("db_session", default=None)
)  # ty: ignore[invalid-assignment]


def get_db_session():
    session = db_session_var.get()
    if session is None:
        raise HTTPException(500, "session is not defined")
    return session


def get_or_set_db_session():
    session = db_session_var.get()
    if session is None:
        session = get_session()
        token = db_session_var.set(session)
        return token, db_session_var.get()
    return None, session
