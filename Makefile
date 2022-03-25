clean:
	rm -rf build dist
package:
	python3 setup.py bdist_wheel 

dist: package
	twine upload dist/* 

test:
	bash -c scripts/test.sh