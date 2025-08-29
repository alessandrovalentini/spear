.PHONY: test lint clean run demo docker-up docker-down deb

test:
	PYTHONPATH=./webservice pytest webservice/tests --cov=webservice --cov-report=xml

lint:
	ruff check webservice --fix

clean:
	# Clean python stuffs
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov coverage.xml

	# Clean deb build
	rm -rf debian/spear debian/.debhelper  debian/spear.postrm.debhelper debian/spear.substvars debian/debhelper-build-stamp
	rm -rf ../spear*.deb ../spear_*.changes ../spear_*.build ../spear_*.tar.gz ../spear_*.buildinfo ../spear_*.dsc

run:
	python webservice/main.py

demo:
	python webservice/main.py --demo

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

docker-down:
	docker compose -f docker/docker-compose.yaml down

deb:
	dpkg-buildpackage -us -uc
