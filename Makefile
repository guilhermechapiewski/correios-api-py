# Makefile for packtrack

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  compile    to compile .py files (just to check for syntax errors)"
	@echo "  test       to execute all simple-db-migrate tests"
	@echo "  install    to install simple-db-migrate"
	@echo "  build      to build without installing"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo

clean:
	@echo "Cleaning..."
	@rm -rf build dist *.pyc **/*.pyc *~ dist packtrack.egg-info

compile: clean
	@echo "Compiling source code..."
	@rm -rf correios/*.pyc
	@rm -rf tests/*.pyc
	@python -tt -m compileall correios
	@python -tt -m compileall tests

test: compile
	# clean again to remove compiled files
	@make clean
	@echo "Starting tests..."
	@export PYTHONPATH="$PYTHONPATH:`pwd`"
	@nosetests -s --verbose --with-coverage --cover-erase --cover-package=correios tests/*
	@make clean

install:
	@/usr/bin/env python ./setup.py install

build:
	@/usr/bin/env python ./setup.py build

dist: clean
	@python setup.py sdist

publish: dist
	@python setup.py sdist upload
