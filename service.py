from dataclasses import dataclass

import aio_pika

from client import MailClient
from schemas import UserMessage


@dataclass
class MailService:
    mail_client: MailClient
    amqp_connection: aio_pika.abc.AbstractConnection

    async def consume_mail(self, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            correlation_id = message.correlation_id
            body = message.body.decode()
            try:
                email_body = UserMessage.parse_raw(body)
                self.mail_client.send_email(
                    subject=email_body.subject,
                    text=email_body.message,
                    to=email_body.user_email,
                )
            except Exception as e:
                await self.send_mail_fail_callback(
                    body=body, correlation_id=correlation_id, error=str(e)
                )

    async def send_mail_fail_callback(self, body: str, correlation_id: str, error: str) -> None:
        channel = await self.amqp_connection.channel()

        # Создание очереди
        queue = await channel.declare_queue('callback_mail_queue', durable=True)

        message = aio_pika.Message(
            body=f"User email: {body} failed with error: {error}".encode(),
            correlation_id=correlation_id,
        )
        await channel.default_exchange.publish(
            message=message,
            routing_key=queue.name,
        )

    def send_email(self, subject: str, text: str, to: str) -> None:
        return self.mail_client.send_email(subject, text, to)
