from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from routers import auth, post, user, opinion
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import pathlib
import os
from db_drive import DB_Driver
from starlette.middleware.cors import CORSMiddleware

load_dotenv(verbose=True, override=True, dotenv_path=f"{pathlib.Path().cwd()}/.env")

app = FastAPI()

# CORS設定
origins = [
    "http://localhost:8080", #Vueのデフォルトポート番号
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db接続の確認
while 1:
    try:
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        # RealDictCursorを使う理由は、jsonに落とし込みやすい
        # https://stackoverflow.com/questions/45399347/psycopg2-dictcursor-vs-realdictcursor
        print("Database connection was successfully")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


app.include_router(auth.router)
app.include_router(opinion.router)
app.include_router(post.router)
app.include_router(user.router)

@app.get("/") # http method & url path
async def root():
    return {"message": "Hello, world!"}

# NOTE : テーブルを削除するとき
# driver = DB_Driver()
# driver.drop_tables()
# driver.create_tables()