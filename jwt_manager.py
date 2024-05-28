from jwt import encode

def create_token(data:dict):
    token: str = encode(payload=data, key="movistar", algorithm="HS256")
    return token