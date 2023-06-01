from celery.utils.log import get_task_logger

from app import celery
from subprocess import run

logger = get_task_logger(__name__)


@celery.task(name='core.tasks.test',
             soft_time_limit=60, time_limit=65)
def test_task():
    logger.info('running test task')
    # Run the pytest command to execute the tests
    result = run(['pytest'], capture_output=True, text=True)
    logger.info(result)
    return True
