# backend apiの実行
run-api:
	cd backend/ && poetry run uvicorn main:app --reload