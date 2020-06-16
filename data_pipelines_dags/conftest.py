"""Global test fixture arrangement.

"""
import os
import tempfile
import logging
import shutil
import pytest


LOG = logging.getLogger(__name__)
if not LOG.handlers:
    LOG.propagate = 0
    CONSOLE = logging.StreamHandler()
    LOG.addHandler(CONSOLE)
    FORMATTER = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    CONSOLE.setFormatter(FORMATTER)

LOG.setLevel(logging.INFO)


@pytest.fixture(scope='function')
def working_dir(request):
    """Temporary working directory.
    """
    def fin():
        """Tear down.
        """
        LOG.info('Deleting working temporay test directory: "%s"', dirpath)
        shutil.rmtree(dirpath)

    request.addfinalizer(fin)
    dirpath = tempfile.mkdtemp()
    LOG.info('Created temporary test directory: "%s"', dirpath)

    return dirpath


def pytest_sessionstart(session):
    """Set up the Airflow context with appropriate config for test.

    """
    dirpath = tempfile.mkdtemp()
    LOG.info('Created Airflow temporary test directory: "%s"', dirpath)

    os.environ['AIRFLOW_HOME'] = dirpath
    os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = os.path.join(dirpath, 'dags')
    os.environ['AIRFLOW__CORE__PLUGINS_FOLDER'] = os.path.join(dirpath, 'plugins')

    from airflow.utils import db
    db.initdb(False)


def pytest_sessionfinish(session, exitstatus):
    """Tear down the Airflow context.

    """
    LOG.info('Deleting working temporay test directory: "%s"', os.environ['AIRFLOW_HOME'])
    shutil.rmtree(os.environ['AIRFLOW_HOME'])
