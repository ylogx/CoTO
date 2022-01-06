lint:
	pipenv run black .

run:
	pipenv run python run.py book-newer-slot

install:
	pipenv install

dev-install:
	pipenv install --dev

sh:
	pipenv shell
