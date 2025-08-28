.PHONY: test lint clean run demo docker-up docker-down

test:
	PYTHONPATH=./webservice pytest webservice/tests --cov=webservice --cov-report=xml

lint:
	ruff check webservice --fix

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov coverage.xml

run:
	python webservice/main.py

demo:
	python webservice/main.py --demo

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

docker-down:
	docker compose -f docker/docker-compose.yaml down
