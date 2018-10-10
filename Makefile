SHELL := /usr/bin/env bash

# TESTARGS = --capture=sys --cov=lightlab --cov-config .coveragerc
TESTARGS = -s -W ignore::UserWarning


venv: venv/bin/activate
venv/bin/activate:
	test -e venv/bin/activate || virtualenv -p python3 --prompt "(lytest-venv) " --distribute venv
	touch venv/bin/activate

clean:
	rm -rf .pytest_cache
	# rm -rf .coverage

purge: clean
	rm -rf venv/*

testbuild: venv requirements.txt
	( \
		source venv/bin/activate; \
		pip install -r requirements.txt | grep -v 'Requirement already satisfied'; \
		pip install -e .; \
	)

test: testbuild
	( \
		source venv/bin/activate; \
		py.test $(TESTARGS) examples; \
	)

.PHONY: test clean purge
