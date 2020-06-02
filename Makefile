include makester/makefiles/makester.mk
include makester/makefiles/python-venv.mk

include envfile
VARS:=$(shell sed -ne 's/ *\#.*$$//; /./ s/=.*$$// p' envfile)
$(foreach v,$(VARS),$(eval $(shell echo export $(v)="$($(v))")))

PROJECT_DIR := $(PWD)/data_pipelines_dags

export PATH := 3env/bin:$(PATH)

package: APP_ENV=prod

export APP_ENV=dev
init:
	$(MAKE) -s makester-requirements
	$(MAKE) -s pip-editable

reset-airflow:
	@$(shell which rm) -fr $(AIRFLOW_HOME)

link-dags:
	@$(shell which ln) -s $(PROJECT_DIR)/dags/ $(AIRFLOW_HOME)
	@$(shell which ln) -s $(PROJECT_DIR)/plugins/ $(AIRFLOW_HOME)

init-db:
	@airflow initdb

pristine: clear-env init reset-airflow version link-dags init-db

start:
	@airflow scheduler & airflow webserver && kill $! || true

CMD ?= --help
airflow:
	@airflow $(CMD)

db-shell: CMD = shell
version: CMD = version
list-dags: CMD = list_dags
run-dag:
	$(shell which echo) "yes" | $(MAKE) airflow CMD="backfill --subdir $(PROJECT_DIR)/dags --reset_dagruns -s 2020-01-01 -e 2020-01-01 $(DAG_TO_RUN)"

db-shell version list-dags: airflow

TESTS ?= $(PROJECT_DIR)/tests
tests:
	PYTHONPATH=$(PROJECT_DIR) $(PYTHON) -m pytest -vv\
 --exitfirst --cov-config .coveragerc\
 --pythonwarnings ignore --cov dags \
 -o junit_family=xunit2 --junitxml junit.xml -sv $(TESTS)

help: makester-help python-venv-help
	@echo "(Makefile)\n\
  init                 Build the local Python-based virtual environment\n\
  reset-airflow        Destroy Airflow environment at \"AIRFLOW_HOME\"\n\
  link-dags            Link project DAGs to Airflow environment at \"AIRFLOW_HOME\"\n\
  init-db              Initialise the Airflow database\n\
  init-connections     Initialise Airflow connections\n\
  init-variables       Initialise Airflow variables\n\
  pristine             Convenience target bundling clear-env, init and reset\n\
  start                Start Airflow in Sequential Executor mode (Ctrl-C to stop)\n\
  airflow              Run any \"airflow\" by setting CMD (defaults to \"CMD=--help\")\n\
  version              Run \"airflow version\" (set CMD=\"version\")\n\
  db-shell             Run \"airflow shell\" (set CMD=\"shell\")\n\
  list-dags            List all the DAGs\n\
  run-dag              Run DAG denoted by \"DAG_TO_RUN\" on the CLI\n\
  tests                Run code test suite\n"

.PHONY: help airflow
