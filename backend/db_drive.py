from models import *
from database import DBAdapter
from typing import List

local_adapter = DBAdapter(  # nosec
    dotenv_path='/Users/gwoninkenji/ShareGratitude/.env',
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

