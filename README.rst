#############################
Data Pipelines - Airflow DAGs
#############################

Airflow DAGs (task level) component of a Data Workflow Management system using these components:

- `Airflow DAGs <https://airflow.apache.org/docs/1.10.10/concepts.html?highlight=dag#core-ideas>`_

The goals here are:

- simple entry point to Airflow DAG development and experimentation
- separate the Airflow DAG component from the heavier, more resource-intensive infrastructure component.  However, a simple `Airflow Sequential Executor-based <https://pypi.org/project/apache-airflow/1.10.10/>`_ instance is available for DAG development
- provide confidence to completely mess up the development environment as it is easily restored

*************
Prerequisties
*************

- `Docker <https://docs.docker.com/install/>`_
- `GNU make <https://www.gnu.org/software/make/manual/make.html>`_

***************
Getting Started
***************

Get the code and change into the top level ``git`` project directory::

    $ git clone https://github.com/loum/data-pipelines-dags.git && cd data-pipelines-dags

.. note::

    Run all commands from the top-level directory of the ``git`` repository.

For first-time setup, get the `Makester project <https://github.com/loum/makester.git>`_::

    $ git submodule update --init

Keep `Makester project <https://github.com/loum/makester.git>`_ up-to-date with::

    $ git submodule update --remote --merge

Setup the environment::

    $ make pristine

.. note::

    The ``pristine`` target will remove and reset all existing Airflow state in ``$(HOME)/airflow``.

**********************
Writing Your First DAG
**********************

The following sample DAG template can help you create your own basic DAG quickly.  The template features a set of ``start`` and ``end`` "book-end" tasks that can be used to delimit your pipeline.  You then add your own Business related tasks in between.

The ``start`` and ``end`` tasks are instantiated via Airflow's `DummyOperators <https://airflow.apache.org/docs/stable/_api/airflow/operators/dummy_operator/index.html?highlight=dummyoperator#airflow.operators.dummy_operator.DummyOperator>`_ and act as *safe* landing zones for your pipeline.

More information around Airflow DAG creation and concepts is available at the `Airflow tutorial <https://airflow.apache.org/docs/stable/tutorial.html>`_.

Create the DAG File
===================

Airflow DAGs are written in Python and are essentially just a Python module (with ``.py`` extension).  DAGs are interpreted by Airflow (via the `DagBag facility <https://airflow.apache.org/docs/stable/_modules/airflow/models/dagbag.html#DagBag>`_) and can then be scheduled to execute.

DAGs files are place under the ``AIRFLOW__CORE__DAGS_FOLDER``.  This can be identified as follows::

    $ make print-AIRFLOW__CORE__DAGS_FOLDER 
    
    AIRFLOW__CORE__DAGS_FOLDER=airflow/dags

Copy the `Sample DAG Template`_ into a new Python file under ``AIRFLOW__CORE__DAGS_FOLDER`` replacing the file header and ``DESCRIPTION`` variable to suit.

.. note::

    Ensure the ``dag_name`` is unique amongst all DAGS under ``AIRFLOW__CORE__DAGS_FOLDER`` as this could cause an implicit conflict that is difficult to troubleshoot.

Sample DAG Template
===================

::

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
