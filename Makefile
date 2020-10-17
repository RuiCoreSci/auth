pip-up:
	pip install --upgrade pip

freeze:
	pip freeze>requirements.txt

pip-install:
	pip install -r requirements.txt

pip-uninstall:
	pip freeze | xargs pip uninstall -y

up:
	docker-compose up -d --remove-orphans
	docker-compose ps

down:
	docker-compose down
	docker-compose ps
