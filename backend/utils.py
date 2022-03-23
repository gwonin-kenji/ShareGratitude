from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    """
    パスワードをハッシュ化して返す
    """
    return pwd_context.hash(password)

def verify(plain_password, hashed_password) -> bool:
    """
    パスワードの一致確認
    """
    return pwd_context.verify(plain_password, hashed_password)