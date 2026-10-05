#!/bin/bash

# source devvenv/bin/activate

watchfiles \
  "celery -A src.utile.celery_conf:celery_app worker" \
  src