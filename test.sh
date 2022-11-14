pip uninstall json_cpp2-0.0.104-cp310-cp310-linux_x86_64.whl -y
python -m pip wheel . --no-deps
pip install json_cpp2-0.0.104-cp310-cp310-linux_x86_64.whl
python test/json_object_tests.py -v