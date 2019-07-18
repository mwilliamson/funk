.PHONY: test test-all upload register clean bootstrap

test:
	sh -c '. _virtualenv/bin/activate; nosetests test'
	_virtualenv/bin/pyflakes funk test
	_virtualenv/bin/rst-lint README.rst

test-all:
	tox

upload: setup test-all
	_virtualenv/bin/python setup.py sdist bdist_wheel upload
	make clean

register: setup
	_virtualenv/bin/python setup.py register

clean:
	rm -f MANIFEST
	rm -rf dist

bootstrap: _virtualenv
	_virtualenv/bin/pip install -e .
ifneq ($(wildcard test-requirements.txt),)
	_virtualenv/bin/pip install -r test-requirements.txt
endif
	make clean

_virtualenv:
	python3 -m venv _virtualenv
	_virtualenv/bin/pip install --upgrade pip
	_virtualenv/bin/pip install --upgrade setuptools
	_virtualenv/bin/pip install --upgrade wheel
