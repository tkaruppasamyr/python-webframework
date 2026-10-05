import logging
from celery import Celery
from contextlib import asynccontextmanager
from fastapi import FastAPI
from celery.signals import (
    setup_logging, task_failure, task_prerun, task_postrun,
    task_retry, task_revoked, task_rejected,
)
from src.core.logging_config import app_setup_logging

celery_app = Celery(
    main="fasapi",
    broker="amqp://fastapi_svc:CHANGE_ME_STRONG_PASSWORD@localhost:5672/fastapi_vhost",
    backend="rpc://",
    include=["src.fileupload.fs_tasks"]
)



# this is celery class loader argument.
celery_app.conf.update(
    # serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,

    # reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    broker_transport_options={"confirm_publish": True},

    # limits
    task_time_limit=300,
    task_soft_time_limit=270,
    worker_max_tasks_per_child=1000,      # recycle processes, avoids memory leaks
    result_expires=3600,

    # monitoring (needed by Flower / exporters)
    worker_send_task_events=True,
    task_send_sent_event=True,
    task_track_started=True,
)

log = logging.getLogger("celery.monitor")

@setup_logging.connect
def configure_logging(**kwargs):
    try:
        app_setup_logging()
    except Exception:
        import traceback
        traceback.print_exc()
        raise

@task_prerun.connect
def on_start(task_id, task, **_):
    log.info("TASK_START name=%s id=%s", task.name, task_id)


@task_postrun.connect
def on_done(task_id, task, state, **_):
    log.info("TASK_DONE name=%s id=%s state=%s", task.name, task_id, state)


@task_failure.connect
def on_failure(sender, task_id, exception, traceback, **_):
    log.error(
        "TASK_FAILED name=%s id=%s error=%r", sender.name, task_id, exception,
        exc_info=(type(exception), exception, traceback),
    )


@task_retry.connect
def on_retry(sender, request, reason, **_):
    log.warning("TASK_RETRY name=%s id=%s reason=%s", sender.name, request.id, reason)


@task_revoked.connect
def on_revoked(sender, request, terminated, expired, **_):
    log.warning("TASK_REVOKED name=%s id=%s expired=%s", sender.name, request.id, expired)


@task_rejected.connect
def on_rejected(sender=None, message=None, **_):
    log.error("TASK_REJECTED sender=%s", sender)


@asynccontextmanager
async def get_celery(app: FastAPI):
    print("Starting Celery...")
    try:
        with celery_app.connection_for_read() as connection:
            connection.ensure_connection(max_retries=3)
            print("Celery connection established.")
    except Exception as e:
        print(f"Failed to connect to Celery: {e}")

    yield

    print("Shutting down Celery...")



from time import sleep

# @celery_app.task(name="add_numbers")
# def add_numbers(x, y):
#     sleep(20)
#     return x + y


