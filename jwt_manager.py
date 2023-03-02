from jwt import encode
from dotenv import dotenv_values

key_doten = dotenv_values(".env")

def create_token(data: dict):
    token:str =encode(payload=data, key= key_doten[TOKEN_LOGIN_KEY], algorithm="HS256")
    return token