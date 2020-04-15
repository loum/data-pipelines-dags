#############################
Data Pipelines - Airflow DAGs
#############################

Airflow DAGs (task level) component of a Data Workflow Management system using these components:

- `Airflow DAGs <https://airflow.apache.org/docs/1.10.10/concepts.html?highlight=dag#core-ideas>`_

The goal here is to separate the Airflow DAG component from the heavier, more resource-intensive infrastructure component.  However, a simple `Airflow Sequential Executor-based <https://pypi.org/project/apache-airflow/1.10.9/>`_ instance is available for the DAG development.

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

    $ make init
