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
	isort -rc .; \
	black . 

test:
	- . .venv/bin/activate; \
	python -m unittest discover

run:
	- . .venv/bin/activate; \
	python bot.py

docker-build:
	docker build -t $(DOCKER_REPO_USER)/mc-aws-discord-assistant:$(TAG) . 

docker-run:
	- docker run --rm --env-file .env $(DOCKER_REPO_USER)/mc-aws-discord-assistant:$(TAG)

docker-push:
	- docker push $(DOCKER_REPO_USER)/mc-aws-discord-assistant:$(TAG)
