include .env
export 

clean:
	- rm -rf .venv

setup: 
	- python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r requirements-dev.txt; \
	pip install -r requirements.txt

update:
	- . .venv/bin/activate; \
	pip install -r requirements-dev.txt; \ 
	pip install -r requirements.txt

format:
	- . .venv/bin/activate; \
	isort -rc; \
	black . 

run:
	- . .venv/bin/activate; \
	python bot/bot.py

docker-build:
	docker build -t $(DOCKER_HOST)/mc-aws-discord-assistant:$(TAG) . 

docker-run:
	- . .env; \
	docker run --rm --env-file .env $(DOCKER_HOST)/mc-aws-discord-assistant:$(TAG)

docker-push:
	- docker push $(DOCKER_HOST)/mc-aws-discord-assistant:$(TAG)
