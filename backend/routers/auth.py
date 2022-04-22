from fastapi import status, HTTPException, Depends, APIRouter
import schemas, utils, oauth2
from models import User
from db_drive import DB_Driver

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

    
@router.post("/login")
def login(user: schemas.UserLogin, db: DB_Driver = Depends(DB_Driver)):
    db_user = db.query_user(user.user_email)

    # ユーザの存在有無
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # パスワードの一致検証
    if not utils.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # TODO : payloadにemailを設定しているが、後々ユーザIDにする
    access_token = oauth2.create_token(data={"user_email": db_user.user_email})
    return {"access_token": access_token, "token_type": "bearer"}


# TODO : ユーザ情報アップデート
# TODO : ユーザ情報削除