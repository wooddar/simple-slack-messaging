dev:
	pip install -r requirements.txt

test:
	bash tests/meta.sh

package:
	python setup.py sdist
	python setup.py bdist_wheel
