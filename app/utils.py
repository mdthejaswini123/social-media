from passlib.context import CryptContext
# to tell the library to use which algorithm to hash the password, we can create a CryptContext object and specify the algorithm we want to use, like this:
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

# function to verify the password, we can use the verify() method of the CryptContext object, which takes the plain password and the hashed password as arguments, and returns True if they match, or False otherwise, like this:


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
