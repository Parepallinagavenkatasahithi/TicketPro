.PHONY: install start build test lint docker

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

start:
	uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 &
	cd frontend && npm run dev

build:
	cd frontend && npm run build

test:
	python -m pytest --cov=backend/app --cov-report=term-missing tests/backend tests/e2e
	cd frontend && npm test

docker:
	docker-compose up --build -d
