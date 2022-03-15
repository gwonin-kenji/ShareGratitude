"""
アプリで必要なdbテーブルとクエリを記述
"""
from ctypes import Union
from typing import Optional
from sqlalchemy import Column, func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY, TEXT, TIMESTAMP, Integer, Date, Boolean
from database import BASE


class User(BASE):
    __tablename__ = 'users'
    id = Column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    user_name = Column(
        TEXT, nullable=False, unique=True, comment='user name'
    )
    password = Column(
        TEXT, nullable=False, comment='user password'
    )
    email = Column(
        TEXT, nullable=False, unique=True, comment='email'
    )
    address = Column(
        TEXT, nullable=True, comment='ユーザの住所'
    )
    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )



class Post(BASE):
    __tablename__ = 'posts'
    id = Column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    content = Column(
        TEXT, nullable=False, comment='感謝の内容'
    )
    mind = Column(
        TEXT, nullable=True, comment='感謝を通しての心の変化'
    )
    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE')
    ) # Foreign key 
    user_name = Column(
        TEXT,
        ForeignKey('users.user_name', onupdate='CASCADE', ondelete='CASCADE')
    ) # Foreign key 


class UserOpinion(BASE):
    __tablename__ = 'opinions'
    id = Column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    content = Column(
        TEXT, nullable=False, comment='感謝の内容'
    )
    tag = Column(
        TEXT, nullable=False, comment='お問合せ/意見/応援メッセージのタグ'
    )    
    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    user_name = Column(
        TEXT,
        ForeignKey('users.user_name', onupdate='CASCADE', ondelete='CASCADE')
    ) # Foreign key 

    # これを外部キーに設定しようとするとエラーが出た。理由はまだ分かってない。 https://teratail.com/questions/144342
    # user_email = Column(
    #     TEXT,
    #     ForeignKey('users.email', onupdate='CASCADE', ondelete='CASCADE')
    # ) # Foreign key 


