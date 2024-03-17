setup:
	poetry run python driver.py

dev:
	poetry run litestar --app miappe.app:app run --debug --reload --pdb


run:
	poetry run litestar --app miappe.app:app run


test:
	poetry run pytest