# # from fastapi import FastAPI, Depends, HTTPException, status
# # from fastapi.security import HTTPBasic, HTTPBasicCredentials
# # from typing import Optional

# # app = FastAPI()

# # security = HTTPBasic()

# # users = {
# #     "ushba": "1234"
# # }

# # def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
# #     correct_username = credentials.username in users
# #     correct_password = users.get(credentials.username) == credentials.password
# #     if not correct_username or not correct_password:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Basic"},
# #         )
# #     return credentials.username

# # def get_current_active_user(current_username: str = Depends(get_current_username)):
# #     if current_username != "admin":
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN,
# #             detail="Not an active user",
# #         )
# #     return current_username

# # @app.get("/admin/login")
# # async def login():
# #     return {"message": "Admin logged in"}

# # @app.get("/admin/protected", dependencies=[Depends(get_current_active_user)])
# # async def protected_endpoint():
# #     return {"message": "This is a protected admin endpoint"}
# import time
# from datetime import datetime, timedelta
# from typing import Optional

# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from pydantic import BaseModel

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = "FA7BACB8BAE16166738B75324BD7E"  # Replace with a strong secret key
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class User(BaseModel):
#     username: str
#     password: str

# users = {
#     "admin": "password"
# }

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = users.get(username)
#     if user is None:
#         raise credentials_exception
#     return user

# def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.username != "ushba":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not an active user",
#         )
#     return current_user

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = users.get(form_data.username)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     if not verify_password(form_data.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user["username"], "exp": access_token_expires}
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/admin/cars", dependencies=[Depends(get_current_active_user)])
# async def get_cars():
#     # Replace with actual logic to fetch cars
#     return {"cars": ["car1", "car2", "car3"]}

# @app.get("/admin/reservations", dependencies=[Depends(get_current_active_user)])
# async def get_reservations():
#     # Replace with actual logic to fetch reservations
#     return {"reservations": ["reservation1", "reservation2"]}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# Secret key for JWT encoding/decoding
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory storage for simplicity (use a database in production)
fake_admin_db = {
    "admin": {"password": "admin_password"}
}

# OAuth2 scheme for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# FastAPI application
app = FastAPI()

# Token Data Model
class TokenData(BaseModel):
    username: str | None = None

# Utility function to verify password
def verify_password(plain_password, hashed_password):
    # Simple password verification (hash in production)
    return plain_password == hashed_password

# Utility function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authenticate admin
def authenticate_admin(username: str, password: str):
    admin = fake_admin_db.get(username)
    if not admin:
        return False
    if not verify_password(password, admin["password"]):
        return False
    return username

# Dependency to get current admin
def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if token_data.username not in fake_admin_db:
        raise credentials_exception
    return token_data.username

# Admin login route
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin_username = authenticate_admin(form_data.username, form_data.password)
    if not admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin_username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route (only for logged-in admins)
@app.get("/protected")
async def read_protected_data(current_admin: str = Depends(get_current_admin)):
    return {"msg": f"Hello, {current_admin}. You are authorized to view this content."}

# Admin logout (token invalidation is handled on the client side by removing the token)
@app.post("/logout")
async def logout():
    # Since JWT tokens are stateless, you can invalidate the token on the client-side.
    # Optionally, you can implement token revocation lists if necessary.
    return {"msg": "Logout successful"}

# Public route
@app.get("/")
async def read_root():
    return {"msg": "Welcome to the public endpoint!"}
