from fastapi import status, HTTPException, Depends, APIRouter
import schemas, utils
from models import User
from db_drive import DB_Driver

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedUserOut)
def create_user(user: schemas.UserCreate, db: DB_Driver = Depends(DB_Driver)):

    user_name = db.query_username(user.user_name)
    if user_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"ユーザ名が重複しています")
    user_email = db.query_email(user.user_email)
    if user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"メールアドレスが重複しています")

    # TODO : パスワードはハッシュ化して保存
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.refresh_query(new_user)
    return new_user