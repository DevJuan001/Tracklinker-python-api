async def invalidate_cache(redis, pattern: str):
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
