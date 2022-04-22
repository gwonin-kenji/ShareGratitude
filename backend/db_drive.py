from models import *
from database import DBAdapter
from typing import List
import os

CURR_DIR_PATH = os.getcwd()

local_adapter = DBAdapter(  # nosec
    dotenv_path=f'{CURR_DIR_PATH}/.env',
    env_db_host='DB_HOST',  # DB_HOST # SD_DB_HOST # MART_DB_HOST
    env_db_name='DB_NAME',  # DB_NAME # SD_DB_NAME # MART_DB_NAME
    env_db_user='DB_USER',  # DB_USER # SD_DB_USER # MART_DB_USER
    env_db_pass='DB_PASS',  # DB_PASS # SD_DB_PASS # MART_DB_PASS
    db_type='postgresql',
)


class DB_Driver:
    def create_tables(self) -> None:
        """
        テーブルの作成
        """
        local_adapter.make_tables(tables=[User])
        local_adapter.make_tables(tables=[Post])
        local_adapter.make_tables(tables=[UserMessage])
    
    def drop_tables(self) -> None:
        """
        テーブルの削除 : 依存関係があるので削除する順番に気を付ける
        """
        local_adapter.delete_tables(tables=[UserMessage])
        local_adapter.delete_tables(tables=[Post])
        local_adapter.delete_tables(tables=[User])

    def add(self, data) -> None:
        """
        保存
        """
        local_adapter.add(data)

    def add_all(self, data_list) -> None:
        """
        複数保存
        """
        local_adapter.add_all(data_list)

    def close_session(self):
        local_adapter.session.close()

    def new_session(self):
        return local_adapter.construct_new_scoped_session()

    def commit(self):
        local_adapter.commit()

    def refresh_query(self, item):
        return local_adapter.refresh_item(item)

    def query_user(self, user_email) -> User:
        """
        引数のemailから、Userオブジェクトを返す
        """
        user = local_adapter.session.query(User).filter(User.user_email == user_email).first()
        return user

    def query_username(self, username) -> str:
        """
        引数のユーザ名と一致するユーザ名を返す
        """
        user_name = local_adapter.session.query(User.user_name).filter(User.user_name == username).first()
        return user_name

    def query_email(self, user_email) -> str:
        """
        引数のemailと一致するemailを返す
        """
        user_email = local_adapter.session.query(User.user_email).filter(User.user_email == user_email).first()
        return user_email
    
    def query_hashed_password(self, user_email) -> str:
        """
        引数のemialで登録されているユーザのパスワードを返す
        """
        password = local_adapter.session.query(User.password).filter(User.user_email == user_email).first()
        return password

    def query_post(self, id):
        post = local_adapter.session.query(Post).filter(Post.id == id)
        return post

    def query_all_posts(self):
        posts = local_adapter.session.query(Post).all()
        return posts