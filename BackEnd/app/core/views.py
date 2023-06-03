
from flask import Blueprint, current_app
from werkzeug.local import LocalProxy


from .tasks import test_task

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'


@core.route('/test', methods=['GET'])
def test():
    logger.info('app test route hit')
    test_task.delay()
    return 'Congratulations! Your core-app test route is running!'
