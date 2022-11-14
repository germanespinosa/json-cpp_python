#!/bin/bash
sudo chmod +666 /var/run/docker.sock

pipx run cibuildwheel --platform linux --archs x86_64

twine upload wheelhouse/*