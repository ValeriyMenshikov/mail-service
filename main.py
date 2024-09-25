from contextlib import asynccontextmanager
from fastapi import FastAPI

from dependency import get_mail_client, get_settings, get_amqp_connection
from service import MailService
from utils import make_amqp_consumer


@asynccontextmanager
async def lifespan(
        app: FastAPI
):
    settings = await get_settings()
    mail_client = await get_mail_client(settings)
    amqp_connection = await get_amqp_connection(settings)
    mail_service = MailService(
        mail_client=mail_client,
        amqp_connection=amqp_connection
    )
    await make_amqp_consumer(
        mail_client=mail_service,
        amqp_connection=amqp_connection
    )
    yield


app = FastAPI(lifespan=lifespan)
