from jose import JWTError, jwt 
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from db_drive import DB_Driver
import schemas
from dotenv import load_dotenv
import os
from typing import Dict

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_token(data: Dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # 期限付きのトークンに更新する

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    """
    トークンで制限をつけているページに対して、ユーザがもつトークンの認証を行う
    """
    try: 
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_email: str = payload.get("user_email")

        if user_email is None:
            raise credentials_exception
        # ユーザに返す構造体を定義する
        token_data = schemas.TokenData(user_email=user_email)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: DB_Driver = Depends(DB_Driver)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )
    # 有効なトークンであればユーザのemailを返す
    token = verify_access_token(token, credentials_exception)
    user = db.query_user(token.user_email)
    return user