python -m pip install --upgrade pip
python -m pip install --user pip-tools
pip-compile --upgrade --extra=dev pyproject.toml -o requirements.txt
python -m pip install --user -r requirements.txt
