from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers
from config import JWT_SECRET
from auth.manager import get_user_manager
from database import User

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600*3)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
