build frontend:
	docker compose up --build Dockerfile.frontend

build backend:
	docker compose up --build Dockerfile.backend

run:
	docker-compose up -d

stop:
	docker-compose down
