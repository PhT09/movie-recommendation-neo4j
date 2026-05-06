from database.connection import driver
from database.crud import register_user, get_user_by_id

def create_user(name: str):
    return register_user(driver, name)

def get_user(user_id: int):
    return get_user_by_id(driver, user_id)
