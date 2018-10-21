SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all: dependencies

fresh: clean dependencies

dependencies:
	if [ ! -d $(ROOT_DIR)/env ]; then python3.6 -m venv $(ROOT_DIR)/env; fi
	source $(ROOT_DIR)/env/bin/activate; yes w | python -m pip install -e .[dev]

clean:
	rm -rf $(ROOT_DIR)/build;
	rm -rf $(ROOT_DIR)/dist;
	rm -rf $(ROOT_DIR)/env;
	rm -rf $(ROOT_DIR)/*.egg-info;
	rm -rf $(ROOT_DIR)/urlparser/*.pyc;

package:
	source $(ROOT_DIR)/env/bin/activate; python setup.py bdist_wheel
