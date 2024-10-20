PYTHON = python3
MANAGE = manage.py
DYNAMO = api/db_manager.py
DYNAMO_DIR = api

.PHONY: test

test: 
	$(PYTHON) $(DYNAMO)	-A
	$(PYTHON) $(MANAGE) test