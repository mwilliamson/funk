.PHONY: test test-xunit

test:
	nosetests test

test-xunit: 
	mkdir build
	nosetests --with-xunit --xunit-file=build/nosetests.xml

clean:
	rm -rf build
	rm -f MANIFEST
	find . -name "*.pyc" -exec rm '{}' ';'
	cd doc; $(MAKE) clean

