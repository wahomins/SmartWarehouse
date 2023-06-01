from celery.utils.log import get_task_logger

from app import celery
from subprocess import run
from app.dbSeed import run_seed

logger = get_task_logger(__name__)


@celery.task(name='core.tasks.test',
             soft_time_limit=60, time_limit=65)
def test_task():
    logger.info('running test task')
    # Run the pytest command to execute the tests
    result = run(['pytest'], capture_output=True, text=True)
    logger.info(result)
    return True

@celery.task(name='core.tasks.seed',
             soft_time_limit=60, time_limit=65)
def seed_task():
    logger.info('running seed task')
    # Run the pytest command to execute the tests
    result = run_seed()
    logger.info(result)
    return True
