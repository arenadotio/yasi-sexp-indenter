PYTHON?=python

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

all: help
.PHONY : all

egg: rst
	${PYTHON} setup.py sdist
.PHONY : egg

dist:
	${PYTHON} setup.py sdist upload
.PHONY : dist

README.rst: README.md
	pandoc --from markdown --to rst --output README.rst README.md

rst: README.rst
.PHONY : rst

htm: README.html
.PHONY : htm

html: README.html
.PHONY : html

README.html: README.rst
	rst2html.py -stg README.rst README.html

py-test:
	@${PYTHON} tests/test_yasi.py
.PHONY : py-test

deps:
	-pip install -r $(ROOT_DIR)/requirements.txt
.PHONY : deps

new-test:
	@newlisp tests/test-yasi-module.lsp
.PHONY : new-test

test: py-test new-test
.PHONY : test

tags: yasi.py
	ctags yasi.py

fmt: yasi.py tests/test_yasi.py
	autopep8 $^ \
		--indent-size=4 \
		--in-place \
		--ignore=E221 \
		--max-line-length 130
.PHONY : fmt

lint:
	-pycodestyle yasi.py tests/test_yasi.py
	@printf "\033[01;36m\n\n-------------------\n\n\033[0m"
	pylint yasi.py tests/test_yasi.py
.PHONY : lint

clean:
	rm -rf __pycache__ tags *.pyc *.bak~ tests/cases/*.bak~
.PHONY : clean

help:
	@echo "Targets:"
	@echo " -> clean"
	@echo " -> deps"
	@echo " -> dist"
	@echo " -> egg"
	@echo " -> fmt"
	@echo " -> htm(html)"
	@echo " -> lint"
	@echo " -> rst"
	@echo " -> tags"
	@echo " -> test(new-test, py-test)"
.PHONY : help
