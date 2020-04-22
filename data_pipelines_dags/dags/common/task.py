"""Set of common, re-useable tasks.

"""
from airflow.operators.dummy_operator import DummyOperator


def start(dag, default_args) -> DummyOperator:
    """Task ``start`` book-end definition.

    """
    return dummy(dag, default_args, 'start')


def end(dag, default_args) -> DummyOperator:
    """Task 'end' book-end definition.

    """
    return dummy(dag, default_args, 'end')


def dummy(dag, default_args, name) -> DummyOperator:
    """Task *name* book-end definition.

    """
    return DummyOperator(task_id=name, default_args=default_args, dag=dag)
