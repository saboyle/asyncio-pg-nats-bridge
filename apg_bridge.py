import asyncio
import json

from nats.aio.client import Client as NATS
import asyncpg

NATS_HOST = 'localhost'
NATS_PORT = '4222'

CHANNEL = 'fixtures.parameters'  # The same channel is configured in both Postgres and NATS (they could be different)


async def bridge(loop):
    async def connect_listener():
        pgconn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1',
                                       loop=loop)
        print("Connected to Postgres")
        await pgconn.add_listener(CHANNEL, publish_update)
        await nc.connect(f"{NATS_HOST}:{NATS_PORT}", loop=loop)

        print("Listener added")

    def publish_update(_con, _pid, _channel, payload):
        asyncio.run_coroutine_threadsafe(nc.publish(CHANNEL, json.dumps(payload).encode('utf-8')), loop)
        logger.info(f"Update received: {payload}")

    nc = NATS()
    await connect_listener()

if __name__ == '__main__':

    import logging

    logging.basicConfig(format='%(asctime)s, %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    event_loop = asyncio.get_event_loop()

    # event_loop.set_debug(True)
    event_loop.run_until_complete(bridge(event_loop))

    try:
        print('Run forever')
        event_loop.run_forever()
    finally:
        print('Closing')
