from fastapi import status, HTTPException, Depends, APIRouter
import schemas
from models import User
from db_drive import DB_Driver

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedUserOut)
def create_user(user: schemas.UserCreate, db: DB_Driver = Depends(DB_Driver)):

    user_name = db.query_username(user.user_name)
    if user_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"ユーザ名が重複しています")
    user_email = db.query_email(user.email)
    if user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"メールアドレスが重複しています")

    # TODO : パスワードはハッシュ化して保存
    new_user = User(**user.dict())
    db.add(new_user)
    db.refresh_query(new_user)
    return new_user
    
@router.post("/login")
def login(user: schemas.UserLogin, db: DB_Driver = Depends(DB_Driver)):
    db_user = db.query_user(user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # TODO : ハッシュ化
    if user.password != db_user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # TODO : トークンの生成
    return {"message": "successfuly logged in"}


# TODO : ユーザ情報アップデート
# TODO : ユーザ情報削除