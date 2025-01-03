from typing import List, Any
from redis.asyncio import Redis


class RedisClient:
    client = Redis(host="redis", port=6379, db=0)

    @classmethod
    async def set_max_hash_ziplist_entries(cls, value: int):
        return await cls.client.config_set("hash-max-ziplist-entries", value)

    @classmethod
    async def get(cls, key: str) -> Any:
        return await cls.client.get(key)

    @classmethod
    async def setex(cls, key: str, expiration_time: int, value: Any):
        return await cls.client.setex(key, expiration_time, value)

    @classmethod
    async def incr(cls, key: str, amount: int = 1):
        return await cls.client.incr(key, amount)

    @classmethod
    async def hsetex(cls, key: str, expiration_time: int, field: str):
        return await cls.client.hexpire(key, expiration_time, field)

    @classmethod
    async def hincrby(cls, key: str, expiration_time: int, field: str):
        return await cls.client.hincrby(key, expiration_time, field)

    @classmethod
    async def set(
        cls,
        key: str,
        value: Any,
        if_already_exists: bool = False,
        keepttl: bool = False,
    ):
        return await cls.client.set(key, value, xx=if_already_exists, keepttl=keepttl)

    @classmethod
    async def delete(
        cls,
        keys: List[str],
    ):
        return await cls.client.delete(*keys)
