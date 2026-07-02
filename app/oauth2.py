
# to create the jwt tken we need 3 things
# 1.a secret key which is a random string of characters that is used to sign the token and verify its authenticity.
# 2. an algorithm which is a cryptographic algorithm that is used to sign the token and verify its authenticity.
# 3. an expiration time which is the time after which the token will no longer be valid and will need to be refreshed or reissued.
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas import TokenData
SECRET_KEY = ""
ALGORITHM = ""
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    # to set the expiration time of the token, we can use the datetime module to get the current time and add the expiration time to it, like this:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # to create the access token, we need to encode the data using the jwt.encode() method, which takes the data, the secret key, and the algorithm as arguments, and returns the encoded token as a string.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
