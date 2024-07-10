from app.common.dao import BaseDao
from .models import UserDoc


class BaseUserDao(BaseDao[UserDoc]):
    def __init__(self):
        super().__init__(UserDoc)


UserDao = BaseUserDao()

# Alternatively, we can just do:
# UserDao = BaseDao(UserDoc)
