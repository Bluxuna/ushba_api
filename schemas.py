from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime
from fastapi import UploadFile
import random
from pydantic import BaseModel, EmailStr

class Admin_schema(BaseModel):
    name: str
    password: str



class Logged_schema(BaseModel):
    admin: bool = False
    cars: bool = False
    reservations: bool = False
    comments: bool = False


class UserSchema(BaseModel):

    name: str
    age: int
    mail: EmailStr | None = None  # Optional email with validation
    phone: str

class CarSchema(BaseModel):

    name: str
    year: int
    fuel_type: str
    engine_type: str
    transmision: str
    seat_amount: int
    doors_amount: int
    max_weight: int
    future_name: str 
    daily_price: int

class PictureSchema(BaseModel):
    picture: UploadFile
    show_index: int

class ReservationSchema(BaseModel):

    user_id: int
    car_id: int
    price: int
    approved: bool

class ReservationDetailsSchema(BaseModel):

    reservation_id: int
    date_from: datetime
    date_to: datetime
    pickup_location: str
    return_location: str
    extra_info: str | None = None

class CommentSchema(BaseModel):
    user_id: int
    comment_text: str
    date: datetime
    show_comment: bool