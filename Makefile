test:
	pytest -v

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

dev:
	gulp --cwd eventsrouter/staticapp/

database:
	dropdb eventsrouter --if-exists
	createdb eventsrouter
