.PHONY: arduino-build arduino-detect arduino-flash arduino-upload clean deb demo docker-down docker-up lint run test

BOARD ?= arduino:avr:nano:cpu=atmega328old
BUILD_DIR ?= ./Arduino/build
SKETCH ?= ./Arduino/multi_ac_current_measure
LIBS_DIR ?= ./Arduino/libraries

arduino-build:
	mkdir -p $(BUILD_DIR)
	arduino-cli core update-index
	arduino-cli core install $(shell echo $(BOARD) | cut -d: -f1,2)
	arduino-cli compile --fqbn $(BOARD) --output-dir $(BUILD_DIR) --libraries $(LIBS_DIR) $(SKETCH)

arduino-upload:
	bash Arduino/upload2board.sh $(BUILD_DIR) $(BOARD)

arduino-flash: arduino-build arduino-upload

clean:
	# Clean python stuffs
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache .coverage htmlcov coverage.xml

	# Clean arduino build
	rm -rf Arduino/build

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