#!/bin/bash

pip uninstall json_cpp2-0.0.104-cp310-cp310-linux_x86_64.whl -y
python -m pip wheel . --no-deps
pip install json_cpp2-0.0.104-cp310-cp310-linux_x86_64.whl

rm docs/modules.rst

rm docs/json_cpp2.rst

sphinx-apidoc -o docs json_cpp2

rm docs/modules.rst

cd docs

make html

cd ..

