lint:
	pipenv run black .

run:
	pipenv run python run.py stb-back-test

irun:
	pipenv run python run.py international-back-test

install:
	pipenv install

dev-install:
	pipenv install --dev

sh:
	pipenv shell
