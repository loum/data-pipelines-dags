"""Common DAG build components for Data Pipeline DAGs.

"""
import os
import datetime
import airflow.utils.dates


class Base:
    """Common components for Data Pipeline DAGs.

    .. attribute:: dag_id

    .. attribute:: default_args

    """
    def __init__(self,
                 dag_name: str,
                 department: str,
                 description: str = None,
                 airflow_env_variable: str = 'AIRFLOW_CUSTOM_ENV',
                 default_args: dict = None,
                 **kwargs):
        """
        *dag_name* and *department* form the :attr:`dag_name` that presents
        in the Airflow dashboard.

        *description* is a brief detail about the DAG.

        *airflow_env_variable* is the name used in the Airflow infrustructure
        environment that determines the instance context.  For example,
        ``local``, ``development`` and ``production``.  Environment naming
        rules are not enforced.

        *default_args* is a dictionary of default parameters to be used as
        constructor keyword parameters when initialising operators

        *kwargs* remaining parameters should represent configuration items to
        :class:`airflow.models.dag.DAG`

        """
        self.__dag_id = f'{department}_{dag_name}_{self.get_env(airflow_env_variable)}'
        self.__description = description
        self.__default_args = default_args
        self.__kwargs = kwargs or {}

    @property
    def dag_id(self):
        """:attr:`dag_id`
        """
        return self.__dag_id.lower()

    @property
    def description(self):
        """:attr:`description`
        """
        return self.__description

    @property
    def default_args(self):
        """Possible DAG ``default_args`` that we may wish to override.

        """
        defaults = {
            'owner': 'airflow',
            'depends_on_past': False,
            'email': [],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 2,
            'retry_delay': datetime.timedelta(minutes=5),
        }
        if self.__default_args:
            defaults.update(self.__default_args)

        return defaults

    @property
    def default_dag_properties(self):
        """Provide sane DAG parameter defaults.
        """
        return {
            'start_date': airflow.utils.dates.days_ago(2),
            'schedule_interval': None,
            'catchup': False,
        }

    @property
    def dag_properties(self):
        """Argument to initialise the DAG.
        """
        return {**(self.default_dag_properties), **(self.__kwargs)}

    @staticmethod
    def get_env(env_variable: str) -> str:
        """Return current environement name.

        String representing the environment name.

        """
        return os.environ.get(env_variable, 'local').upper()
