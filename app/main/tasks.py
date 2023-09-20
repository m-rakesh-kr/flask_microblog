import time
from app import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class MailException(Exception):
    pass


@celery.task()
def print_hello():
    logger.info("Hello")


@celery.task()
def every_minute_add(a, b):
    result = a + b
    logger.info(f"Result of {a} + {b} is {result}")
    return result


@celery.task()
def every_minute_multiply(a, b):
    result = a + b
    logger.info(f"Result of {a} * {b} is {result}")
    return result

