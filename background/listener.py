import asyncio
import json
import logging
import traceback

import async_timeout
from redis.asyncio.client import PubSub

from app.LandAPI.context import AppContext
from app.dependencies import get_context
from app.entities import State

listener = None


class Listener:

    def __init__(self):
        self.task = None
        self.pubsub = None

    async def get_context(self):
        return await get_context().__anext__()

    async def listen(self):
        ctx = await self.get_context()
        redis = ctx.redis
        self.pubsub = await redis.pubsub()
        await self.pubsub.subscribe(**{redis.config.telemetry_channel: self.listen_telemetry,
                                       })
        self.task = asyncio.create_task(self.run(self.pubsub))

    async def listen_telemetry(self, msg):
        data = json.loads(msg['data'])
        state = State(**data)
        ctx = await self.get_context()
        task = asyncio.create_task(state.save(ctx))
        task.add_done_callback(lambda context: asyncio.create_task(AppContext.done_callback(ctx)))

    async def stop(self):
        self.task.cancel()

    async def run(self, channel: PubSub):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=1)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
            except Exception as exc:
                logging.log(logging.ERROR, exc)
                traceback.print_exc()


def create_listener():
    global listener
    listener = Listener()
    return listener


def get_listener():
    global listener
    return listener
