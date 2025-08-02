.PHONY: test lint clean run demo-up demo-down

test:
	PYTHONPATH=. pytest --cov=. --cov-report=term-missing -v

lint:
	ruff check . --fix

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov

run:
	uvicorn main:app --host 0.0.0.0 --port 8000

demo-up:
	docker compose -f docker/docker-compose.yaml up

demo-down:
	docker compose -f docker/docker-compose.yaml down
