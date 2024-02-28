# Makefile

.PHONY: run down log restart

run:
	docker-compose -f docker-compose.yml up -d --build
restart:
	docker-compose -f docker-compose.yml restart
down:
	docker compose -f docker-compose.yml down --remove-orphans
log:
	docker-compose logs -f api
