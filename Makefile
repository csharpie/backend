test:
	REUSE_DB=1 ./manage.py test

setup:
	pip install -r requirements.txt
	psql -f ./sql/setup.sql

seed:
	psql -f ./sql/seed_data.sql
