all: build run

build:
	docker-compose build

run:
	docker-compose run --rm --service-ports develop

test__%:
	python -m tests.$(subst test__,,$@)__tests
