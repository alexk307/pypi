#!/usr/bin/env bash

python setup.py sdist
python setup.py register -r pypi
twine upload dist/*