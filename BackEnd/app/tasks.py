from celery import shared_task
from .dbSeed import run_seed

@shared_task
def execute_seed():
    run_seed()
