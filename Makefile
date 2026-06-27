build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -docer

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local,yml logs

show-logs-api:
	docker compose -f local.yml logs api

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic
	--no-input --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect src_local_postgres_data

authors-db:
	docker compose -f local.yml exec postgres psql --username=davood
	--dbname=authors-live

flake8:
	docker compose -f local.yml exec api flake8 .

black-check:
	docker compose -f local.yml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec api black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec api black --exclude=migrations .

isort-check:
	docker compose -f local.yml exec api isort . --check-only --skip venv
	--skip migrations

isort-diff:
	docker compose -f local.yml exec api isort . --diff --skip venv --skip
	migrations

isort:
	docker compose -f local.yml exec api isort . --skip venv --skip migrations

pytest-cov:
	docker compose -f local.yml run --rm api pytest -p no:warnings --cov=. -v

pytest-cov-html:
	docker compose -f local.yml run --rm api pytest -p no:warnings --cov=. --cov-report html

check-deploy:
	docker compose -f local.yml run --rm api python manage.py check --deploy

install-portainer:
	sudo docker run -d -p 8000:8000 --network=reverseproxy_nw --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest