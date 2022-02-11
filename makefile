
clean:
	-rm -r build/*
	find src/ -name '*.pyc' -exec rm -f {} +
	find src/ -name '*.pyo' -exec rm -f {} +
	find src/ -name '*~' -exec rm -f {} +
	find src/ -name '__pycache__' -exec rm -fr {} +
	find src/ -name '*.htm' -exec rm -f {} +
	find src/ -name '*.html' -exec rm -f {} +
	find src/ -name '*.so' -exec rm -f {} +
	-rm -r dist/*
	-rm -r src/*.egg-info

install:
	pip install -v -e .

test:
	PYCGIR_DEBUG=1 pytest
	python verification/verify.py
