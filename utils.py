from typing import Annotated
from fastapi import Depends
import aio_pika

from dependency import get_mail_service, get_amqp_connection
from service import MailService
from settings import Settings

settings = Settings()


async def make_amqp_consumer(
        mail_client: Annotated[MailService, Depends(get_mail_service)],
        amqp_connection: Annotated[aio_pika.abc.AbstractConnection, Depends(get_amqp_connection)]
) -> None:
    channel = await amqp_connection.channel()
    queue = await channel.declare_queue("email_queue", durable=True)
    await queue.consume(mail_client.consume_mail)
