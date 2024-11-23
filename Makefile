compile:
	uv run pyside6-uic view/tree.ui -o view/tree.py

run:
	uv run python app.py