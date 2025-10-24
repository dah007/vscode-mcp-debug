PROJECT_NAME := fastapi_app
ZIP_NAME := $(PROJECT_NAME).zip

.PHONY: clean zip

clean:
	@echo "🧹 Cleaning project..."
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' -o -name 'build' -o -name 'dist' -o -name '.pytest_cache' -o -name '.venv' -o -name 'venv' -o -name '.env' -o -name 'env' \) -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.log' -o -name '.coverage' \) -delete

zip: clean
	@echo "📦 Creating zip archive..."
	zip -r $(ZIP_NAME) . -x "*.git*" "*__pycache__*" "*.pyc" "*.pyo" "*.log" "*.coverage" "*.egg-info*" "build/*" "dist/*" ".venv/*" "venv/*" ".env" "env/*" ".pytest_cache/*" ".vscode/*" ".idea/*"
	@echo "✅ Created $(ZIP_NAME)"

.PHONY: check-endpoints
check-endpoints:
	@echo "Running endpoint checks..."
	@scripts/check_endpoints.sh