from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
import schemas
from models import Post
from db_drive import DB_Driver

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# TODO : ポスト作成 初めは誰でも作成できるようにする。トークンでの制限は後程
@router.post("/create", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: DB_Driver = Depends(DB_Driver)):
    # TODO : トークンでユーザを確認したら、感謝ポストの外部キーにユーザidを設定するようにupdateする処理をつける
    new_post = Post(**post.dict())
    db.add(new_post)
    db.refresh_query(new_post)
    return new_post


# TODO : トークンで制限をつける
@router.put("/update/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: DB_Driver = Depends(DB_Driver)):
    post_query = db.query_post(id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} is not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# TODO : 削除
@router.delete("/delete/{id}")
def delete_post(id: int, db: DB_Driver = Depends(DB_Driver)):
    post = db.query_post(id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# TODO : 表示
@router.get("/", response_model=List[schemas.SharePost])
def get_all_posts(db: DB_Driver = Depends(DB_Driver)):
    posts = db.query_all_posts()
    return posts

# TODO : トークンで制限をつけたとしてもトークンを持ったユーザが別のユーザのidを入力した場合、みることができるのではないか、、
@router.get("/{id}")
def get_user_post(id: int, db: DB_Driver = Depends(DB_Driver)):
    # 現在はパスにidを入力している仕様だが、トークンで制限をつけた後は、そのユーザのidに紐づいているポストを表示するって形で良さそうだ。
    db.query_user()