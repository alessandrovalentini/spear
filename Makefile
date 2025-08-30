.PHONY: arduino clean deb demo docker-down docker-up lint run test

arduino:
	mkdir Arduino/build
	arduino-cli core update-index
	arduino-cli core install arduino:avr
	arduino-cli compile --fqbn arduino:avr:nano --output-dir ./Arduino/build --libraries ./Arduino/libraries ./Arduino/multi_ac_current_measure

clean:
	# Clean python stuffs
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov coverage.xml

	# Clean deb build
	rm -rf debian/spear debian/.debhelper  debian/spear.postrm.debhelper debian/spear.substvars debian/debhelper-build-stamp
	rm -rf ../spear*.deb ../spear_*.changes ../spear_*.build ../spear_*.tar.gz ../spear_*.buildinfo ../spear_*.dsc

deb:
	dpkg-buildpackage -us -uc

demo:
	python webservice/main.py --demo

docker-down:
	docker compose -f docker/docker-compose.yaml down

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

lint:
	ruff check webservice --fix

run:
	python webservice/main.py

test:
	PYTHONPATH=./webservice pytest webservice/tests --cov=webservice --cov-report=xml