"""
RQ worker entrypoint. Run inside the worker container:
    python -m app.workers.run
"""
from __future__ import annotations

import sys

from loguru import logger
from redis import Redis
from rq import Queue, Worker

from app.core.config import settings


def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level)
    logger.info("Worker starting — env={}", settings.env)

    conn = Redis.from_url(settings.redis_url)
    queues = [Queue("default", connection=conn)]
    worker = Worker(queues, connection=conn)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
