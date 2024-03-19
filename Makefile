CMD=poetry run
MODULE=miappe

dev:
	$(CMD) litestar --app $(MODULE).app:app run --debug --reload


prod:
	$(CMD) litestar --app $(MODULE).app:app run


test:
	$(CMD) pytest --cov-report term-missing --cov=$(MODULE) --cov-report=xml


lint:
	$(CMD) ruff check $(MODULE)


analysis:
	$(CMD) mypy $(MODULE)


clean:
	clear
	rm -rf *.sqlite