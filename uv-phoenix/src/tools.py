import random
import time
from phoenix_config import TRACER

TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_db_info",
            "description": "Fetch a list of users from a database. This tool can only be used by users who are authorized. Make sure to use the auth_user tool before using this tool.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "required": []
        }
    },
    {
        "type": "function",
        "function": {
            "name": "auth_user",
            "description": "Authenticate a user with a password. Need username and password.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["username", "password"]
            },
            "required": []
        }
    }
]

@TRACER.tool()
def fetch_db_info():
    # 1-3秒のランダム遅延
    delay = random.uniform(1.0, 3.0)
    time.sleep(delay)
    
    # 10%の確率で失敗
    if random.random() < 0.1:
        raise RuntimeError("Failed to fetch users data")
    
    # ダミーのユーザーデータを生成して返す
    dummy_users = [
        {"id": 1, "name": "Taro Tanaka", "email": "tanaka@example.com", "age": 28},
        {"id": 2, "name": "Hana Sato", "email": "sato@example.com", "age": 34},
        {"id": 3, "name": "Suzuki Ichiro", "email": "suzuki@example.com", "age": 42},
        {"id": 4, "name": "Yuko Ito", "email": "ito@example.com", "age": 25},
        {"id": 5, "name": "Ken Yamada", "email": "yamada@example.com", "age": 31}
    ]
    
    return dummy_users

@TRACER.chain()
def get_password(username):
    passwords = {
        "ais_user": ["aishift2025"],
        "admin": ["admin_master_password"]
    }
    return passwords[username]

@TRACER.chain()
def get_auth_users():
    users = ["ais_user", "admin"]
    return users

@TRACER.tool()
def auth_user(username, password):
    auth_users = get_auth_users()
    auth_password = get_password(username)
    if password in auth_password and username in auth_users:
        return "Authorized"
    else:
        return "Not authorized"

