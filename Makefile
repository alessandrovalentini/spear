.PHONY: test lint clean run demo docker-up docker-down

test:
	PYTHONPATH=. pytest --cov=. --cov-report=xml

lint:
	ruff check . --fix

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov

run:
	python main.py

demo:
	python main.py --demo

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

docker-down:
	docker compose -f docker/docker-compose.yaml down
