compile:
	uv run pyside6-uic view/tree.ui -o view/tree.py

run:
	make compile
	uv run python app.py

design:
	uv run pyside6-designer view/tree.ui
