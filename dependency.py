from typing import Annotated
from fastapi import Depends
from client import MailClient
from service import MailService
from settings import Settings
import aio_pika


async def get_settings(
) -> Settings:
    return Settings()


async def get_mail_client(
        settings: Annotated[Settings, Depends(get_settings)]
) -> MailClient:
    return MailClient(settings=settings)


async def get_amqp_connection(
        settings: Annotated[Settings, Depends(get_settings)]
) -> aio_pika.abc.AbstractConnection:
    return await aio_pika.connect_robust(settings.RABBIT_URL)


async def get_mail_service(
        mail_client: Annotated[MailClient, Depends(get_mail_client)],
        amqp_connection: Annotated[aio_pika.abc.AbstractConnection, Depends(get_amqp_connection)]
) -> MailService:
    return MailService(mail_client=mail_client, amqp_connection=amqp_connection)
