import random

from fastapi import FastAPI, HTTPException, status, File, UploadFile, Body, Depends
# from fastapi.security  import 
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from models import *
from schemas import *
from settings import UPLOAD_FOLDER, FOLDER_PATH, user,password
from extentions import get_hash
import shutil
# from twilio.rest import Client
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.responses import FileResponse
# mail libraries
# import smtplib
# from email.message import EmailMessage
# telegram libraries
import asyncio
import telegram
# from telegram import Bot
# mail sender functionality from
# def send_email( subject, body, to):
#     user = 'giorgimaxara5@gmail.com'
#     password = 'tmim ltzc wlcp nvvt'

#     msg = EmailMessage()
#     msg['from'] = user
#     msg['to'] = to
#     msg['Subject'] = subject
#     msg.set_content(body)
#     body_bytes = msg.as_bytes()
#     # view = memoryview(body_bytes)
#     # byte_view = view.cast("B")

#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.starttls()
#         smtp.login(user, password)  # Replace with your password
#         smtp.send_message(msg)
#     print("mail send")


# def send_reservation(info: str):
    
#     account_sid = 'AC78b6305c73bc1aa55bbfc599ee2cf982'
#     auth_token = 'a97074a015fe7577345930434552d5f1'
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         from_='whatsapp:+14155238886',
#         body=f'{info}',
#         to='whatsapp:+995598311309'
#     )

#     print(message.sid)
# logged = Logged_schema()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = FastAPI()

engine = create_engine("sqlite:///ushba3.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


# -----------------------------------------------------


# Secret key for JWT encoding/decoding
SECRET_KEY = "FA7BACB8BAE16166738B75324BD7E"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# telegram bot token----------------------
# bot_token = '7369046862:AAFZfY9rd0Xrf6K6HDBTs788q8E3hBPV__M'
# bot = telegram.Bot(token=bot_token)
# # telegram bot function
async def send_message_to_user(user_id, message):
    try:
        bot_token = '7369046862:AAFZfY9rd0Xrf6K6HDBTs788q8E3hBPV__M'
         bot = telegram.Bot(token=bot_token)

        await bot.send_message(chat_id=user_id, text=message)
        print("Message sent successfully!")
    except telegram.TelegramError as e:
        print(f"Error sending message: {e}")

# OAuth2 scheme for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin_gate")

# FastAPI application


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
    admin = dbsession.query(Admin).where(username == Admin.name).first()
    print(admin.name == username)
    # admin = fake_admin_db.get(username)
    if not admin:
        return False
    if not verify_password(str(get_hash(password)), admin.password):
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
            print("test2")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        print("test1")
        raise credentials_exception
    data = dbsession.query(Admin).where(token_data.username == Admin.name).first()
    if not data:
    # if token_data.username not in fake_admin_db:
    #     print("test")
        raise credentials_exception
    return token_data.username

# Admin login route




# -------------------------------------------------pictures action

def make_name(filename: str, id: str, temp: str,idx: int):
    final_name = ""
    x = filename.split('.')
    final_name += id
    final_name += (temp + str(idx))

    final_name += ('.' + x[1])

    return final_name


# ----------------------------------------------------------------------------------------------------------------


def save_files(files: list, carid: int):
    idx=0
    for file in files:
        full_path = ""
        tmp = f"G{random.randint(1, 141241212)}"
        print("File from saving",file)
        if file.filename == '':
            return "no file"
        if file:  # and allowed_file(file.filename):
            print(file.filename, type(file.filename))
            # filename = secure_filename(file.filename)

            filename = make_name(file.filename, str(carid), str(tmp), idx)
            full_path += FOLDER_PATH+filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            # aq gaiwereba fotos damateba bazashi
            pictureId = random.randint(1,1313121213)
            new_img = Picture(pictureId,carid,full_path,idx)
            dbsession.add(new_img)
            idx+=1
    dbsession.commit()
# ----------------------------------------------------------------
@app.get("/")
def main():
    return {"info":"main_page"}
@app.get('/comments')
def main_page():
    commnets = dbsession.query(Comment).where(Comment.show_comment == True).all()
    cars = dbsession.query(Car).all()



    return {"cooments":commnets,"cars":cars}

@app.post('/comment')
async def add_comment(name: str,number:str, comment: str):
    user_data = dbsession.query(User).where(User.name==name and User.phone==number).first()
    reservation_data = dbsession.query(Reservation).where(Reservation.user_id == user_data.id).first()
    if reservation_data:
        comment_id = random.randint(1,13413431)
        date = datetime.now()
        comment_for_db = Comment(id=comment_id,user_id=user_data.id,comment_text=comment,date=date,show_comment=True)
        dbsession.add(comment_for_db)
        dbsession.commit()
        return {"info":"კომენტარი დამატებულია"}
    else:
        return {"info": "კომენტარი ვერ დაემატება რადგან ის ჩვენი მომხმარებელი არ არის"}

# es unda shevasworo
@app.get('/cars')
def cars():
    cars = dbsession.query(Car).all()
    print(type(cars[0]))
    return {"cars": cars}

@app.get('/cars/{carID}')
def car(carid: int):
    car = dbsession.query(Car).where(Car.id == carid).first()
    pics = dbsession.query(Picture).where(Picture.car_id == carid).all()

    return {"car":car,"pics":[i.path for i in pics]}



@app.post('/cars/{carid}')
async def reservation(
        carid: int,
        user_name: str,
        user_age: int,
        user_mail: str,
        user_phone: str,
        date_from: datetime,
        date_to: datetime,
        pickup_location: str,
        return_location: str,
        extra_info: str):
    if user_age>=25:
        reservation_id = random.randint(1, 1341342134)
        reservation_details_id = random.randint(1, 1341342134)
        user_id = random.randint(1, 1341342134)
        user = User(id=user_id, name=user_name,user_age=user_age,mail=user_mail,phone=user_phone)
        car = dbsession.query(Car).where(Car.id==carid).first()

        reservation = Reservation(id=reservation_id,user_id=user_id, car_id=carid, price=car.daily_price, approved=False)
        reservation_details = Reservation_details(id=reservation_details_id, reservation_id=reservation_id, date_from=date_from, date_to=date_to, pickup_location=pickup_location, return_location=return_location, extra_info=extra_info)
        dbsession.add(user)
        dbsession.add(reservation)
        dbsession.add(reservation_details)
        dbsession.commit()
        reservation_info = f""" 
        user_name:{user_name},
        user_age:{user_age},
        user_phone: {user_phone},
        connect_user: f"https://wa.me/{user_phone}"
        car_info : {car.name,car.transmision,car.daily_price},
        date_from: {date_from},
        date_to: {date_to},
        pickup_location: {pickup_location},
        return_location: {return_location},
        extra_info: {extra_info}
        """
        try:
            user_id = 5937741258
            await send_message_to_user(user_id, reservation_info)
            send_email("მანქანის ჯავშანი", reservation_info, "ninikheladze9@gmail.com")
            # send_reservation(reservation_info)

        except Exception:
            print("message is not send")
        return {"reservation" : "is made"}


@app.post('/reservation')
async def reservation(name: str, phone_number:str):
    user = dbsession.query(User).where(User.name==name and User.phone==phone_number).first()
    data = dbsession.query(Reservation).where(Reservation.user_id==user.id).all()
    if data:
        return {"reservation info" : data}




@app.post("/admin_gate")
async def admin_gate(form_data: OAuth2PasswordRequestForm = Depends()):
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

@app.get('/admin')
async def admin(current_admin: str = Depends(get_current_admin)):
        return {"info":"აქ გამოჩნდება ყველა გვერდის ლინკი რაც სამართავია ადმინ პანელიდან"}


@app.get('/admin/cars')
def admin_all_cars(current_admin: str = Depends(get_current_admin)):
    cars = dbsession.query(Car).all()
    return {"cars": cars}

@app.get('/admin/car/{carid}')
def admin_all_cars(carid: int, current_admin: str = Depends(get_current_admin)):

    car = dbsession.query(Car).where(Car.id==carid).one()
    pics = dbsession.query(Picture).where(Picture.car_id == carid).all()

    return {"car": car, "pics": [i.path for i in pics]}
    
@app.post('/admin/car')
def add_cars(   
    name: str,
    year: int,
    fuel_type: str,
    engine_type: str,
    transmision: str,
    seat_amount: int,
    doors_amount: int,
    max_weight: int,
    future_name: str,
    daily_price: int,
    pics: List[UploadFile] = File(...),
    current_admin: str = Depends(get_current_admin)
):
    print(current_admin)
    carId = random.randint(1,133123)
    futureId = random.randint(1,133123)
    car = Car(carId,name,year,fuel_type,engine_type,transmision,seat_amount,doors_amount,max_weight,daily_price)
    future = Car_future(futureId,carId,future_name)
    dbsession.add(future)
    dbsession.add(car)
        
    print(car)
    save_files(pics, carId)
    print("pictures saved")

    dbsession.commit()
    return {"INFO":"DATA SAVED  "}

@app.get('/admin/reservations')
async def show_reservations(current_admin: str = Depends(get_current_admin)):
    print(current_admin)
    reservations = dbsession.query(Reservation).all()

    return {"reservations":reservations}


@app.get('/admin/reservations/{reservaion_id}')
async def see_reservationn(reservation_id:int, current_admin: str = Depends(get_current_admin)):
        print(current_admin)
        reservation = dbsession.query(Reservation).where(Reservation.id==reservation_id).first()
        if reservation:
            return reservation
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="მსგავსი ჯავშანი არ არსებობს")
        
@app.post('/admin/reservations/{reservaion_id}')
async def submit_reservation(reservation_id: int, submit: bool, current_admin: str = Depends(get_current_admin)):
        print(current_admin)
        reservation = dbsession.query(Reservation).where(Reservation.id==reservation_id).first()
        if reservation and submit == True:
            reservation.approved = True
            dbsession.commit()
            return {"info":"reservation is made"}
        else:
            dbsession.delete(reservation)
            dbsession.commit()
            return {"info":"reservation is empty"}

 

@app.get('/admin/comments')
async def show_comments(current_admin: str = Depends(get_current_admin)):

        data = dbsession.query(Comment).all()

        return data

@app.post("/admin/comment")
async def admin_comments(
    user_name: str,
    comment_text: str,
    show_comment: bool,
    current_admin: str = Depends(get_current_admin)
):

    
        userid = random.randint(1,12313123123123)
        user_name = user_name
        user_age = random.randint(25,68)
        text = comment_text
        date = datetime.now()
        show_comment = show_comment
        commentid = random.randint(1,12313123123123)
        user = User(userid,user_name,user_age,mail='',phone='111111111')
        comment = Comment(commentid,userid,text,date,show_comment)
        
        dbsession.add(user)
        dbsession.add(comment)
        dbsession.commit()

        return HTTPException(status_code=status.HTTP_202_ACCEPTED,detail="comment added")
  
    
@app.delete('/admin/comment/{comment_id}')
def delete_comment(
    comment_id: int,
    current_admin: str = Depends(get_current_admin)
):


        comment_query = dbsession.query(Comment).filter(Comment.id == comment_id).first()

        if comment_query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"COMMENT with id {comment_id} not found")
        
        dbsession.execute(delete(Comment).where(Comment.id == comment_id))
        dbsession.commit()

        return {"message": f"COMMENT with id {comment_id} deleted successfully"}
    

    
