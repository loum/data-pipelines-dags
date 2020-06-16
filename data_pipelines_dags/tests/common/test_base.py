""":class:`dags.common.Base` unit test cases.
"""
import datetime

import dags.common


def test_base_init():
    """Initialise a dags.common.Base object.
    """
    # Given a DAG load name
    load_name = 'sample-staging'

    # and description
    description = """Test DAG"""

    # and a department
    department = """Department"""

    # when I initialise a dags.common.Base object
    base = dags.common.Base(load_name, department, description)

    # I should get a dags.common.Base instance
    msg = 'Object is not a dags.common.Base instance'
    assert isinstance(base, dags.common.Base), msg

    # and the dag_id generates
    msg = 'dag_id error'
    assert base.dag_id == 'department_sample-staging_local', msg


def test_default_args_override():
    """dags.common.Base Operator default_arg overridee.
    """
    # Given a DAG load name
    load_name = 'sample-staging'

    # and a department
    department = """Department"""

    # and an overriden Operator parameter
    operator_params = {
        'owner': 'AIRFLOW',
        'retry_delay': datetime.timedelta(minutes=60),
    }

    # when I initialise a dags.common.Base object
    base = dags.common.Base(load_name, department, default_args=operator_params)

    # I should get an overriden Operator parameter data structure
    msg = 'Overriden Operator default_args error'
    expected = {
        'owner': 'AIRFLOW',
        'depends_on_past': False,
        'email': [],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': datetime.timedelta(minutes=60)
    }
    assert base.default_args == expected, msg


def test_dag_params_override():
    """dags.common.Base Dag parameter override.
    """
    # Given a DAG load name
    load_name = 'sample-staging'

    # and a department
    department = """Department"""

    # and an overriden Operator parameters
    dag_params = {
        'start_date': datetime.datetime(2020, 1, 1),
        'end_date': datetime.datetime(2021, 12, 31),
        'schedule_interval': '@daily',
    }

    # when I initialise a dags.common.Base object
    base = dags.common.Base(load_name,
                            department,
                            **dag_params)

    # I should get an overriden DAG parameter data structure
    msg = 'Overriden DAG parameter error'
    expected = {
        'catchup': False,
        'start_date': datetime.datetime(2020, 1, 1),
        'end_date': datetime.datetime(2021, 12, 31),
        'schedule_interval': '@daily',
    }
    assert base.dag_properties == expected, msg
