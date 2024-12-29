from typing import Any
from redis.asyncio import Redis


class RedisClient:
    client = Redis(host="redis", port=6379, db=0)

    @classmethod
    async def get(cls, key: str) -> Any:
        return await cls.client.get(key)

    @classmethod
    async def setex(cls, key: str, expiration_time: int, value: Any):
        return await cls.client.setex(key, expiration_time, value)

    @classmethod
    async def set(
        cls,
        key: str,
        value: Any,
        if_already_exists: bool = False,
        keepttl: bool = False,
    ):
        return await cls.client.set(key, value, xx=if_already_exists, keepttl=keepttl)
