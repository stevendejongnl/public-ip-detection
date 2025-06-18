.PHONY: image run

TELEGRAM_CHAT_ID ?= NOT_SET
TELEGRAM_BOT_TOKEN ?= NOT_SET

run: image
	docker run --rm -it \
		-e PYTHONPATH=/app \
		-e PYTHONUNBUFFERED=1 \
		-e TELEGRAM_CHAT_ID=$(TELEGRAM_CHAT_ID) \
		-e TELEGRAM_BOT_TOKEN=$(TELEGRAM_BOT_TOKEN) \
		-v $(shell pwd):/app \
		--name public-ip-detection \
		public-ip-detection:latest

image:
	docker build --tag public-ip-detection:latest .

