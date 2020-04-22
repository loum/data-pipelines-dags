include makester/makefiles/makester.mk
include makester/makefiles/python-venv.mk

include envfile
VARS:=$(shell sed -ne 's/ *\#.*$$//; /./ s/=.*$$// p' envfile)
$(foreach v,$(VARS),$(eval $(shell echo export $(v)="$($(v))")))

export PATH := 3env/bin:$(PATH)

init:
	$(MAKE) makester-requirements
	$(MAKE) pip-requirements

reset-airflow:
	@$(shell which rm) -fr $(AIRFLOW_HOME)

link-dags:
	@$(shell which ln) -s $(PWD)/dags/ $(AIRFLOW_HOME)
	@$(shell which ln) -s $(PWD)/plugins/ $(AIRFLOW_HOME)

pristine: clear-env init reset-airflow version link-dags
	@airflow initdb

backoff:
	@$(PYTHON) makester/scripts/backoff -d "Airflow web UI" -p $(AIRFLOW__WEBSERVER__WEB_SERVER_PORT) localhost

start-sequential:
	@airflow scheduler & airflow webserver && kill $! || true

start: start-sequential backoff

CMD ?= --help
airflow:
	@airflow $(CMD)

db-shell: CMD = shell
version: CMD = version

db-shell version trigger: airflow

TESTS?=dags/common/tests/test_base.py

tests:
	@PYTHONPATH=. python -m pytest -vv\
 --exitfirst --cov-config .coveragerc\
 --pythonwarnings ignore --cov dags \
 -o junit_family=xunit2 --junitxml junit.xml -sv $(TESTS)

help: makester-help python-venv-help
	@echo "(Makefile)\n\
  init                 Build the local Python-based virtual environment\n\
  reset-airflow        Destroy Airflow environment at \"AIRFLOW_HOME\"\n\
  link-dags            Link project DAGs to Airflow environment at \"AIRFLOW_HOME\"\n\
  pristine             Convenience target bundling clear-env, init and reset\n\
  backoff              Wait until Airflow instances are available\n\
  start-sequential     Start Airflow in Sequential Executor mode (Ctrl-C to stop)\n\
  start                Start Airflow in Sequential Executor mode (Ctrl-C to stop) and wait for services\n\
  airflow              Run any \"airflow\" by setting CMD (defaults to \"CMD=--help\")\n\
  version              Run \"airflow version\" (set CMD=\"version\")\n\
  db-shell             Run \"airflow shell\" (set CMD=\"shell\")\n\
  tests                Run code test suite\n"

.PHONY: help
