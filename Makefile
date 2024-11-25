default: install run

install: install-bot-service install-connector-service

export POSTGRES_DB=expenses
export POSTGRES_USER=darwinai
export POSTGRES_PASSWORD=darwinai
export DB_HOST=localhost
export DB_PORT=5432
export OPENAI_API_KEY=sk-
export TELEGRAM_TOKEN=8071685814:AAE3KmXABZwFg5beAuiSJ8501z1QzSwJtpE
export BOT_SERVICE=http://127.0.0.1:8000/

install-bot-service:
	cd bot-service && docker compose up -d && poetry install;


install-connector-service:
	cd connector-service && yarn install;

run: run-bot-service run-connector-service

run-bot-service:
	cd bot-service && poetry run uvicorn app.main:app &

run-connector-service:
	cd connector-service && yarn start

test: test-bot-service

test-bot-service:
	cd bot-service && poetry run pytest
