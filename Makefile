include .env
export 

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