# Table Football App Makefile
# Simplifies common Django commands using Docker

# Define Docker service name
DOCKER_SERVICE = web

.PHONY: help makemigrations migrate createsuperuser runserver shell test clean collectstatic docker-up docker-down docker-build logs test-urls

# Default target
help:
	@echo "Available commands:"
	@echo "  make help              - Show this help message"
	@echo "  make makemigrations    - Create database migrations"
	@echo "  make migrate           - Apply database migrations"
	@echo "  make createsuperuser   - Create a superuser account"
	@echo "  make runserver         - Run development server"
	@echo "  make shell             - Open Django shell"
	@echo "  make test              - Run tests"
	@echo "  make test-urls         - Run URL tests"
	@echo "  make clean             - Remove Python compiled files"
	@echo "  make collectstatic     - Collect static files"
	@echo "  make docker-up         - Start Docker containers"
	@echo "  make docker-down       - Stop Docker containers"
	@echo "  make docker-build      - Build Docker containers"
	@echo "  make logs              - View Docker logs"

# Database operations
makemigrations:
	docker-compose run --rm $(DOCKER_SERVICE) python manage.py makemigrations

migrate:
	docker-compose run --rm $(DOCKER_SERVICE) python manage.py migrate

# User management
createsuperuser:
	docker-compose run --rm $(DOCKER_SERVICE) python manage.py createsuperuser

# Development server
runserver:
	docker-compose up

# Django shell
shell:
	docker-compose run --rm $(DOCKER_SERVICE) python manage.py shell

# Testing
test:
	docker-compose run --rm $(DOCKER_SERVICE) pytest -v

test-urls:
	docker-compose run --rm $(DOCKER_SERVICE) pytest scores/tests/test_urls.py -v

# Clean up compiled Python files
clean:
	docker-compose run --rm $(DOCKER_SERVICE) bash -c "find . -name '*.pyc' -delete && find . -name '__pycache__' -delete"

# Static files
collectstatic:
	docker-compose run --rm $(DOCKER_SERVICE) python manage.py collectstatic --noinput

# Docker commands
docker-up:
	docker-compose up

docker-down:
	docker-compose down

docker-build:
	docker-compose build

# View logs
logs:
	docker-compose logs -f
