.PHONY: test

test:
	nosetests test

clean:
	rm MANIFEST
	find . -name "*.pyc" -exec rm '{}' ';'
	cd doc; $(MAKE) clean

