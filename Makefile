include makester/makefiles/base.mk
include makester/makefiles/python-venv.mk

init: 
	$(MAKE) makester-requirements
	$(MAKE) pip-requirements

help: base-help python-venv-help
	@echo "(Makefile)\n\
  init                 Build the local Python-based virtual environment\n"

.PHONY: help
