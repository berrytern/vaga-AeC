from typing import List
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
                self.host,
                self.port,
                self.username,
                self.password,
                use_tls=True,
                start_tls=True,
            )
            await self.__connection.connect(tls_context=context)
        return self.__connection

    async def send_email(self, recipients: List[str], subject: str, body: str):
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = ", ".join(recipients)

        connection = await self.connection()
        return await connection.sendmail(self.username, recipients, message.as_string())
