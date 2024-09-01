import random

from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from models import *
from extentions import get_hash
engine = create_engine("sqlite:///ushba.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
psswrd = get_hash("bluxuna")
randm = random.randint(1,1212112)

admin = Admin(id=randm,name='giorgi',password=psswrd)


dbsession.add(admin)
dbsession.commit()

