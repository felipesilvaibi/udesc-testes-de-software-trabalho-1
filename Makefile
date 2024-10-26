run:
	uv run uvicorn main:app --reload --app-dir src

test:
	uv run pytest -v

export_requirements:
	uv pip freeze > requirements.txt
