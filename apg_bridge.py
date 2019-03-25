import asyncio
import json

from nats.aio.client import Client as NATS
import asyncpg

NATS_HOST = 'localhost'
NATS_PORT = '4222'

############################
# IN PROGRESS - DO NOT USE
############################


async def bridge(loop):
    async def connect_listener():
        pgconn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1')
        await pgconn.add_listener('fixtures.parameters', publish_update)

    async def publish_update(msg):
        data = json.loads(msg.data.decode('utf-8'))
        logger.info('Processing {}'.format(data["uid"]))
        logger.debug('In mh_s1 with {}'.format(data))
        idata = json.loads(msg.data.decode('utf-8'))
        rdata = {'uid': str(idata['uid']), 'claim_id': idata['uid']}

        await nc.publish("p1.s1", json.dumps(rdata).encode('utf-8'))

    nc = NATS()
    await nc.connect(f"{NATS_HOST}:{NATS_PORT}", loop=loop)
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
