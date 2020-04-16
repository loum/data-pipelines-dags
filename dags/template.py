"""The simplest DAG template.

"""
import airflow

import common
import common.task

DESCRIPTION = """Simple book-end DAG template to get you started"""

BASE = common.Base(dag_name='template-DAG', department='coles', description=DESCRIPTION)

DAG = airflow.DAG(BASE.dag_id,
                  default_args=BASE.default_args,
                  **(BASE.dag_properties))

TASK_START = common.task.start(DAG, BASE.default_args)
TASK_END = common.task.end(DAG, BASE.default_args)

TASK_START >> TASK_END
