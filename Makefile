setup:

	pip install -r requirements.txt
	mypy routes.py
	flake8 --ignore=E501 routes.py
