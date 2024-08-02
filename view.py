from fastapi import FastAPI, HTTPException, status, File, UploadFile, Body
from typing import Optional
import os
import models
from settings import host
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from models import *
from schemas import *
from settings import UPLOAD_FOLDER, FOLDER_PATH, user,password
from extentions import get_hash
import shutil


logged = Logged_schema()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = FastAPI()

engine = create_engine("sqlite:///ushba2.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
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
            
            dbsession.commit()
            idx+=1
# ----------------------------------------------------------------

@app.get('/')
def main_page():
    commnets = dbsession.query(Comment).where(Comment.show_comment == True).all()
    cars = dbsession.query(Car).all()

    return {"cooments":commnets,"cars":cars}


@app.post('/')
async def main_post(data: str):
    print(data)
    return {"request made": True}

@app.post('/admin_gate')
async def admin_gate(
        login_info: Admin_schema
):
    error = None
    hashed_name = get_hash(login_info.name)
    hashed_password = get_hash(login_info.password)

    if hashed_name != user and hashed_password != password:
        error = "არ შეიძლება პაროლი არასწორია"
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="შესვლა არ შეიძლება პაროლი არასწორია")
    logged.admin = True
    raise HTTPException(status_code=status.HTTP_200_OK, detail="შესვლა ნებადართულია")

@app.get('/admin')
async def admin():
    if logged.admin:
        logged.cars = True
        logged.reservations = True
        logged.comments = True
        return {"info":"აქ გამოჩნდება ყველა გვერდის ლინკი რაც სამართავია ადმინ პანელიდან"}
    else:
        return {"info" : "შენ არ გაქვს აქ შემოსვლის უფლება"}



@app.post('/admin')
async def admin_route(
        logout: bool | None = None,
):

    if logged.admin:
        if logout:
            logged.admin = False
            logged.cars = False
            logged.comments = False
            logged.reservations = False
            raise HTTPException(status_code=status.HTTP_200_OK,detail="შენ გამოხვედი ადმინ პანელიდან")
        return " admin panel"
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="შენ არ გაქვს აქ შესვლის უფლება")
    
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
    pics: List[UploadFile] = File(...)
):

    if logged.cars:
        carId = random.randint(1,133123)
        car = Car(carId,name,year,fuel_type,engine_type,transmision,seat_amount,doors_amount,max_weight,daily_price)
        dbsession.add(car)
        print(car)
        save_files(pics, carId)
        print("pictures saved")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="შენ არ გაქვს აქ შესვლის უფლება")
    

@app.get('/admin/comments')
async def show_comments():
    if logged.admin:
        data = dbsession.query(Comment).all()
        return data
    else:
        return "you do not have a permition"

@app.post("/admin/comment")
async def admin_comments(admin_comment: CommentSchema):
    if logged.comments:
    
        userid = random.randint(1,12313123123123)
        user_name = admin_comment.user_name
        text = admin_comment.comment_text
        date = admin_comment.date
        show_comment = admin_comment.show_comment
        commentid = random.randint(1,12313123123123)
        user = User(userid,user_name,mail=None,phone=None)
        comment = Comment(commentid,userid,text,date,show_comment)
        
        dbsession.add(user)
        dbsession.add(comment)
        dbsession.commit()
        return HTTPException(status_code=status.HTTP_202_ACCEPTED,detail="comment added")
    else:
        return "you do not have a permition"
    
@app.delete('/admin/comment/{comment_id}')
def delete_comment(comment_id: int):
    if logged.comments:    
        comment_query = dbsession.query(Comment).filter(Comment.id == comment_id).first()
        if comment_query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"COMMENT with id {comment_id} not found")
        dbsession.execute(delete(Comment).where(Comment.id == comment_id))
        dbsession.commit()
        return {"message": f"COMMENT with id {comment_id} deleted successfully"}
    else:
        return "you do not have a permition"