import asyncio
import logging
from aiokafka import AIOKafkaProducer
from sqlalchemy import select, update
from app.database import Session
from app.core.config import settings
from app.models.outbox import Outbox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbox_worker")


async def process_outbox(producer: AIOKafkaProducer):
    async with Session() as session:
        result = await session.execute(
            select(Outbox).where(Outbox.sent == False).order_by(Outbox.id)
        )
        messages = result.scalars().all()

        if not messages:
            return

        for msg in messages:
            msg_id = msg.id
            msg_event_type = msg.event_type
            try:
                await producer.send_and_wait(msg_event_type, str(msg.payload).encode())
                await session.execute(
                    update(Outbox).where(Outbox.id == msg_id).values(sent=True)
                )
                await session.commit()
                logger.info(f"Outbox id={msg_id} отправлен в топик {msg_event_type}")
            except Exception as e:
                await session.execute(
                    update(Outbox)
                    .where(Outbox.id == msg_id)
                    .values(retry_count=Outbox.retry_count + 1)
                )
                await session.commit()
                logger.error(f"Ошибка отправки outbox id={msg_id}: {e}")


async def main():
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    logger.info("Outbox worker запущен")

    try:
        while True:
            await process_outbox(producer)
            await asyncio.sleep(2.5)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
