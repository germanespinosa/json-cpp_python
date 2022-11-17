version=$(cat version)
pip uninstall json_cpp2-$version-cp310-cp310-linux_x86_64.whl -y
python -m pip wheel . --no-deps
pip install json_cpp2-$version-cp310-cp310-linux_x86_64.whl
(
cd tests
python test_basic.py
python ../json_cpp2/json_list.py
python ../json_cpp2/json_object.py
python ../json_cpp2/json_parser.py
rm *.json
)

