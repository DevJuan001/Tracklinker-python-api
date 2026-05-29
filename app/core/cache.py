import json


async def set_cache(redis, key: str, data, ex: int = 20):
    await redis.set(key, json.dumps(data), ex=ex)


async def get_cache(redis, key: str):
    cached = await redis.get(key)
    return json.loads(cached) if cached else None


async def invalidate_cache(redis, pattern: str):
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
