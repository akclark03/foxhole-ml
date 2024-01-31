worker:
	psql -U postgres -h 127.0.0.1 pgml_development -f foxhole/db/schema.sql
	poetry run python peak/worker.py