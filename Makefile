dev:
	pip install -r requirements.txt

test:
	bash tests/meta.sh

package:
	python setup.py sdist
	python setup.py bdist_wheel
	black ./simple_slack --check
	mypy ./simple_slack
	pytest ./simple_slack
	codecov


