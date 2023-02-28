DOCKER_ENV := deploy/.env
LOCAL_ENV := .env

ifneq (${DOCKER},)
	ENV_FILE := ${DOCKER_ENV}
else ifeq (${DOCKER},)
	ENV_FILE := ${LOCAL_ENV}
endif

include ${ENV_FILE}
export

all:
	echo ${POSTGRES_HOST} && echo ${ENV_FILE} && echo " "

 .PHONY: migrate-up
migrate-up:
	poetry run alembic -c ./playlist/adapters/sqlalchemy/alembic.ini upgrade head

 .PHONY: migrate-down
migrate-down:
	poetry run alembic -c ./playlist/adapters/sqlalchemy/alembic.ini downgrade $(revision)

 .PHONY: migrate-create
migrate-create:
	poetry run alembic -c ./playlist/adapters/sqlalchemy/alembic.ini revision --autogenerate -m $(name)

 .PHONY: migrate-history
migrate-history:
	poetry run alembic -c ./playlist/adapters/sqlalchemy/alembic.ini history

 .PHONY: migrate-stamp
migrate-stamp:
	poetry run alembic -c ./playlist/adapters/sqlalchemy/alembic.ini stamp $(revision)

 .PHONY: run-tests
run-tests:
	poetry run pytest -v -s

 .PHONY: generate-proto
generate-proto:
	poetry run python3.11 -m grpc_tools.protoc \
	-I ./playlist/adapters/grpc/protos \
	--python_out=./playlist/adapters/grpc/generated \
	--pyi_out=./playlist/adapters/grpc/generated \
	--grpc_python_out=./playlist/adapters/grpc/generated \
	./playlist/adapters/grpc/protos/$(path)

 .PHONY: run-service
run-service:
	poetry run python3.11 -m playlist.adapters.grpc.bootstrap

 .PHONY: compose-build
compose-build:
	docker-compose -f ./deploy/docker-compose.yml --env-file ${DOCKER_ENV} build

 .PHONY: compose-up
compose-up:
	docker-compose -f ./deploy/docker-compose.yml --env-file ${DOCKER_ENV} up -d

 .PHONY: compose-logs
compose-logs:
	docker-compose -f ./deploy/docker-compose.yml --env-file ${DOCKER_ENV} logs -f

 .PHONY: compose-exec
compose-exec:
	docker-compose -f ./deploy/docker-compose.yml --env-file ${DOCKER_ENV} exec backend bash

 .PHONY: docker-rm-volume
docker-rm-volume:
	docker volume rm -f workout_postgres_data

 .PHONY: compose-down
compose-down:
	docker-compose -f ./deploy/docker-compose.yml --env-file ${DOCKER_ENV} down --remove-orphans