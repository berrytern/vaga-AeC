from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
import ssl


class EmailClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.__connection = None

    async def connection(self):
        context = ssl.create_default_context()
        if self.__connection is None or not self.__connection.is_connected:
            self.__connection = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True,
            )
            await self.__connection.connect(tls_context=context)
        return self.__connection

    async def send_email(self, recipients: List[str], subject: str, *parts: MIMEText):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = ", ".join(recipients)
        for part in parts:
            msg.attach(part)

        connection = await self.connection()
        return await connection.sendmail(self.username, recipients, msg.as_string())
