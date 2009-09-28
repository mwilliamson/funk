.PHONY: test

test:
	nosetests test

clean:
	find . -name "*.pyc" -exec rm '{}' ';'
	cd doc; $(MAKE) clean

