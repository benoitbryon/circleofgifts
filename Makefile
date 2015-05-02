# Makefile for development.
PYTHON = $(shell which python)
PROJECT = $(shell $(PYTHON) -c "import setup; print setup.NAME")
PIP = pip
NOSE = nosetests


configure:
	# Configuration is stored in etc/ folder. Not generated yet.


develop:
	pip install -e .
	pip install nose coverage rednose


clean:
	find . -name "*.pyc" -delete
	find . -name ".noseids" -delete


distclean: clean
	rm -rf *.egg-info


maintainer-clean: distclean


test:
	$(NOSE) --config etc/nose.cfg $(PROJECT)
	coverage erase
