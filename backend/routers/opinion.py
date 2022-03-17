from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
import schemas
from models import UserMessage
from db_drive import DB_Driver
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
SLACKWEBHOOK = os.environ.get("WEBHOOK")

router = APIRouter(
    prefix="/message",
    tags=["Opinion and Message"]
)

# tagが意見だったら、フロントはこのapiを叩く
@router.post("/opinion")
def create_opinion(card: schemas.UserOpinionSupport, db: DB_Driver = Depends(DB_Driver)):
    # slackに通知する処理
    # TODO : slackへの通知をもう少しカスタマイズする & 応援メッセージ用とお問い合せ意見用に分ける
    requests.post(
        SLACKWEBHOOK,
        data = json.dumps({
            "username": card.user_email,
            "text": card.content
        })
    )
    # DBに保存する処理
    msg = UserMessage(**card.dict())
    db.add(msg)
    db.refresh_query(msg)
    return msg

# tagが応援だったら、フロントはこのapiを叩く
@router.post("/support")
def create_message(card: schemas.UserOpinionSupport, db: DB_Driver = Depends(DB_Driver)):
    # slackに通知
    # TODO : slackへの通知をもう少しカスタマイズする & 応援メッセージ用とお問い合せ意見用に分ける
    requests.post(
        SLACKWEBHOOK,
        data = json.dumps({
            "username": card.user_email,
            "text": card.content
        })
    )
    # DBに保存する処理
    msg = UserMessage(**card.dict())
    db.add(msg)
    db.refresh_query(msg)
    return msg