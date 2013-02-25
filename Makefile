# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'django-downloadview'
ROOT_DIR = $(shell pwd)
WGET = wget
PYTHON = python
BUILDOUT_CONFIGURATION = $(ROOT_DIR)/etc/buildout/buildout.cfg
BUILDOUT_BOOTSTRAP_URL = https://raw.github.com/buildout/buildout/1.6.3/bootstrap/bootstrap.py
BUILDOUT_BOOTSTRAP = $(ROOT_DIR)/lib/buildout/bootstrap.py
BUILDOUT = $(ROOT_DIR)/bin/buildout
BUILDOUT_ARGS = -N -c $(BUILDOUT_CONFIGURATION)


develop: buildout


buildout:
	# Download zc.buildout bootstrap.
	if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then \
		mkdir -p $(ROOT_DIR)/lib/buildout; \
		$(WGET) -O $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_URL); \
	fi
	# Generate buildout's local directory configuration.
	if [ ! -f $(ROOT_DIR)/etc/buildout/directories-local.cfg ]; then \
		echo "[buildout]" > $(ROOT_DIR)/etc/buildout/directories-local.cfg; \
		echo "directory = $(ROOT_DIR)" >> $(ROOT_DIR)/etc/buildout/directories-local.cfg; \
	fi
	# Bootstrap buildout.
	if [ ! -x $(BUILDOUT) ]; then \
		$(PYTHON) $(BUILDOUT_BOOTSTRAP) --distribute -c $(BUILDOUT_CONFIGURATION); \
	fi
	# Run zc.buildout.
	$(BUILDOUT) $(BUILDOUT_ARGS)


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/
