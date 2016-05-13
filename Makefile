.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using nose"
	@echo "  production  run test suite and do a release"
	@echo "  release     package and upload a release"
	@echo "  sdist       package"

production: clean test release

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	rm -fr build \
	rm -fr dist \
	find . -name '*.pyc' -exec rm -f {} \
	find . -name '*.pyo' -exec rm -f {} \
	find . -name '*~' -exec rm -f {}

install:
	make deps
	make test

lint:
	flake8 insynsregistret > violations.flake8.txt

test:
	/usr/local/bin/nosetests --nocapture

release: register
	python setup.py sdist upload

register:
	python setup.py register

sdist:
	python setup.py sdist
