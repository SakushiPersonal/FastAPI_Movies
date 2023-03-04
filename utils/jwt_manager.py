from jwt import encode, decode
from dotenv import dotenv_values

key_doten = dotenv_values(".env")

#Create a new token
def create_token(data: dict):
    token:str =encode(payload=data, key= key_doten["TOKEN_LOGIN_KEY"], algorithm="HS256")
    return token

#Validate your token
def validate_token(token:str) -> dict:
    data:dict = decode(token, key=key_doten["TOKEN_LOGIN_KEY"], algorithms=['HS256'])
    return data
