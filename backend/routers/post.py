from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
import schemas, oauth2
from models import Post
from db_drive import DB_Driver

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/create", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: DB_Driver = Depends(DB_Driver), 
    current_user = Depends(oauth2.get_current_user),
    ):
    # TODO : トークンでユーザを確認したら、感謝ポストの外部キーにユーザidを設定するようにupdateする処理をつける
    new_post = Post(**post.dict())
    db.add(new_post)
    db.refresh_query(new_post)
    return new_post

@router.put("/update/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: DB_Driver = Depends(DB_Driver),
    current_user = Depends(oauth2.get_current_user),
    ):
    post_query = db.query_post(id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} is not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/delete/{id}")
def delete_post(
    id: int, 
    db: DB_Driver = Depends(DB_Driver),
    current_user = Depends(oauth2.get_current_user),    
    ):
    # TODO : ログインさえすれば誰でも削除できるので、トークンから取得できるユーザメールから、ユーザ名を取得し、外部キーが同じユーザ名の投稿を削除できるようにする
    # 1. 外部キー(owner_id)が、user_idと一致するポストをクエリする
    # 2. ポストがあれば削除する

    post = db.query_post(id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.get("/", response_model=List[schemas.SharePost])
def get_all_posts(db: DB_Driver = Depends(DB_Driver)):
    posts = db.query_all_posts()
    return posts

# TODO : トークンで制限をつけたとしてもトークンを持ったユーザが別のユーザのidを入力した場合、みることができるのではないか、、
@router.get("/{id}")
def get_user_post(
    id: int, 
    db: DB_Driver = Depends(DB_Driver),
    current_user = Depends(oauth2.get_current_user),    
    ):
    # 現在はパスにidを入力している仕様だが、トークンで制限をつけた後は、そのユーザのidに紐づいているポストを表示するって形で良さそうだ。
    db.query_user()