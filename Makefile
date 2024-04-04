# Makefile

.PHONY: run down log restart coverage report pre-commit bandit

run:
	docker-compose -f docker-compose.yml up -d --build
restart:
	docker-compose -f docker-compose.yml restart
down:
	docker compose -f docker-compose.yml down --remove-orphans
log:
	docker-compose logs -f api
coverage:
	coverage run -m pytest tests/unit tests/integration
report:
	coverage report -m
	coverage html
pre-commit:
	pre-commit run --all-files
bandit:
	bandit --configfile pyproject.toml -r src tests
