include secrets/coin.env
export

backup_file := pg_$(shell date "+%Y_%m_%d_%H:%M:%S").zip
project_name := COIN_BOT
compose_file := dockerfiles/docker-compose.yml
compose := docker-compose -f $(compose_file) -p $(project_name)

build:
	$(compose) build --parallel

up_db:
	$(compose) up -d db

migrate:
	sleep 1
	poetry run python src/migrate.py

install: build up_db
	$(compose) up -d

ps:
	$(compose) ps -a $(service)

top:
	$(compose) top $(service)

logs:
	$(compose) logs -f $(service)

destroy_data:
	find ./ -name 'data' -print0 | xargs -0 --no-run-if-empty rm -r

create_backup:
	zip -rv $(backup_file) data
