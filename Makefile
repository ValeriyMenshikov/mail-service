.DEFAULT_GOAL := help

run:
	uvicorn main:app --host 0.0.0.0 --port 8082 --reload

grun: ## Run the application using uvicorn with provided arguments or defaults
	gunicorn app.main:app -c gunicorn.conf.py


help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'