PYTHON = python3
BACKEND_DIR = backend
FRONTEND_DIR = frontend

run_backend:
	# @source env/bin/activate
	cd $(BACKEND_DIR) && PYTHON manage.py runserver

run_frontend: 
	cd $(FRONTEND_DIR) && npm run dev

run_all: run_backend run_frontend
