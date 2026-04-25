from redis import Redis
from rq import Queue

from app.core.config import settings

redis_client: Redis = Redis.from_url(settings.redis_url, decode_responses=True)

# Queue uses a separate connection (rq needs bytes)
_rq_redis = Redis.from_url(settings.redis_url)
default_queue = Queue("default", connection=_rq_redis)


def cache_get(key: str) -> str | None:
    return redis_client.get(key)


def cache_set(key: str, value: str, ttl: int = 3600) -> None:
    redis_client.set(key, value, ex=ttl)
