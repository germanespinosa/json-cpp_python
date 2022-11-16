python -m pip wheel . --no-deps
pipx run cibuildwheel --platform linux --archs x86_64
pipx run cibuildwheel --platform linux --archs aarch64
python -m twine upload wheelhouse/*