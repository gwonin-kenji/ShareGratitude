from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    """
    パスワードをハッシュ化して返す
    """
    return pwd_context.hash(password)
