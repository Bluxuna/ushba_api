# models.py არის ფაილი რომელშიც აღწერილია  ბაზის თეიბლების მონაცემების ტიპები

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine




Base = declarative_base()





class User(Base):

    __tablename__ = "User"

    id = Column('user_id', Integer, primary_key=True, nullable=False)
    name = Column("full_name", String, nullable=False)
    age = Column("age", Integer,nullable=False)

    mail = Column("user_mail", String, nullable=True)
    phone = Column("user_phone", String, nullable=False)
    def __init__(self, id: int, name: str, mail: str, phone: str):
        self.id = id
        self.name = name
        self.mail = mail
        self.phone = phone

    def __repr__(self):
        return f"id:{self.id} name:{self.name} mail:{self.mail} phone:{self.phone}"





class Car(Base):

    __tablename__ = 'Car'

    id = Column("car_id", Integer, nullable=False, primary_key=True)
    name = Column("name", String, nullable=False)
    year = Column("year", Integer, nullable=False)
    fuel_type = Column("fuel_type", String, nullable=False)
    engine_type = Column("engine_type", String, nullable=False)
    transmision = Column("transmision", String, nullable=False)
    seat_amount = Column('seat_amount', Integer, nullable=False)
    doors_amount = Column("doors_amount", Integer, nullable=False)
    max_weight = Column('max_weight', Integer, nullable=False)
    daily_price = Column('daily_price', Integer, nullable=True)

    def __init__(self, id: int, name: str, year: int,fuel_type: str, engine_type: str, transmision: str,
                 seat_amount: int, doors_amount: int, max_weight: int, daily_price:int =0 ):
        self.id = id
        self.name = name
        self.year = year
        self.fuel_type = fuel_type
        self.engine_type = engine_type
        self.transmision = transmision
        self.seat_amount = seat_amount
        self.doors_amount = doors_amount
        self.max_weight = max_weight
        self.daily_price = daily_price

    def __repr__(self):
        return f"id:{self.id} name:{self.name} year:{self.year}  fuel_type:{self.fuel_type} engine_type:{self.fuel_type}  transmition : {self.transmision} seat_amount:{self.seat_amount} door_amount:{self.doors_amount} max_weight:{self.max_weight} daily_price:{self.daily_price}"




class Car_future(Base):

    __tablename__ = 'Car_future'

    future_id = Column('car_future_id', Integer, nullable=False, primary_key=True)
    car_id = Column("car_id", Integer, ForeignKey('Car.car_id'), nullable=True)
    future_name = Column('future_name', String, nullable=True)

    car = relationship('Car', backref='car_future')

    def __init__(self, id: int, car_id: int, future_name:str):
        self.future_id = id
        self.car_id = car_id
        self.future_name = future_name
    def __repr__(self):
        return f"future_id:{self.future_id} car_id:{self.car_id} future_name:{self.future_name}"


class Picture(Base):

    __tablename__ = "Picture"

    picture_id = Column('picture_id', Integer, nullable=False, primary_key=True)
    car_id = Column("car_id", Integer, ForeignKey("Car.car_id"), nullable=False)
    path = Column('path', String, nullable=False)
    show_index = Column('show_index', Integer, nullable=False)

    car = relationship('Car', backref='picture')

    def __init__(self, id: int, car_id: int, path: str, show_index: int ):
        self.picture_id = id
        self.car_id = car_id
        self.path = path
        self.show_index = show_index

    def __repr__(self):
        return f"id:{self.picture_id} car_id:{self.car_id} path:{self.path}, show_index:{self.show_index}"


class Reservation(Base):

    __tablename__ = "Reservation"

    id = Column("reservation_id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('User.user_id'), nullable=False)
    car_id = Column("car_id", Integer, ForeignKey("Car.car_id"), nullable=False)
    price = Column("price", Integer)
    approved = Column("approved", Boolean)

    car = relationship('Car', backref='Reservation')
    user = relationship('User', backref='Reservation')

    def __init__(self, id: int, user_id: int, car_id: int, price: int , approved:bool):
        self.id = id
        self.user_id = user_id
        self.car_id = car_id
        self.price = price
        self.approved = approved

    def __repr__(self):
        return f"id:{self.picture_id} car_id:{self.car_id} path:{self.path}, show_index:{self.show_index}"



class Reservation_details(Base):
    __tablename__ = "reservation_details"

    id = Column("reservation_details", Integer, nullable=False, primary_key=True)
    reservation_id = Column("reservation_id", Integer, ForeignKey('Reservation.reservation_id'), nullable=False)
    date_from = Column("from", DateTime, nullable=False)
    date_to = Column("to", DateTime, nullable=False)
    pickup_location = Column("pickup_location", Text, nullable=False)
    return_location = Column("return_location", Text, nullable=False)
    extra_info = Column("extra_info", Text)

    reservation = relationship('Reservation', backref='Reservation_date')

    def __init__(self, id: int, reservation_id: int, date_from: DateTime, date_to: DateTime, pickup_location: str, return_location: str, extra_info: str):
        self.id = id
        self.reservation_id = id
        self.date_from = date_from
        self.date_to = date_to
        self.pickup_location = pickup_location
        self.return_location = return_location
        self.extra_info = extra_info

    def __repr__(self):
        return f"id:{self.id} reservation_id:{self.reservation_id} date_from:{self.date_from} date_to:{self.date_to} pickup_location:{self.pickup_location} return_location:{self.return_location} extra info {self.extra_info}"


class Comment(Base):

    __tablename__ = "Comment"

    id = Column('comment_id', Integer, nullable=False, primary_key=True)
    user_id = Column('user_id', Integer,ForeignKey('User.user_id'), nullable=False)
    comment_text = Column('comment_text', Text, nullable=False)
    date = Column('comment_date', DateTime, nullable=False)
    show_comment = Column('comment_show', Boolean, nullable=False)

    user = relationship('User', backref='Comment')

    def __init__(self, id: int, user_id: int, comment_text: str, date:DateTime, show_comment: Boolean):
        self.id = id
        self.user_id = user_id
        self.comment_text = comment_text
        self.date = date
        self.show_comment = show_comment

    def __repr__(self):
        return f"id:{self.id} user_id:{self.user_id} comment_text:{self.comment_text} comment_date:{self.date} comment_show:{self.show_comment}"


# connection_string = "sqlite:///ushba2.db"
# engine = create_engine(connection_string, echo=True)
# Base.metadata.create_all(bind=engine, checkfirst=True)
# file already created do not uncomment it blux  !!!!!
# Check if database file exists
# DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST = settings.user, settings.paassword,settings.host
# if not os.path.exists("ushba.db"):
#     engine = create_engine(
#         f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/your_database_name"
#     )
#     # engine = create_engine(f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}", echo=True)
#     Base.metadata.create_all(bind=engine)
# else:
#     engine = create_engine(f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}", echo=True)
