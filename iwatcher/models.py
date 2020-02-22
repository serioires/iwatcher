import datetime
from peewee import *
from flask import g

DATABASE = 'iwatcher_test'
DBUSER = 'iwatcher-test'
DBPASS = 'testpassword'
db = MySQLDatabase(DATABASE,user=DBUSER,password=DBPASS)

#общий прототип для моделей
class BaseModel(Model):
    class Meta():
        database = db


class User(BaseModel):
    username = TextField(unique=True)
    password = TextField()
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    joined = TimestampField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.username


class Camera(BaseModel):
    lat = IntegerField()
    lon = IntegerField()
    dev = SmallIntegerField()
    author = ForeignKeyField(User, backref='cameras')
    added = DateField(default = datetime.date.today())
    about = TextField(null = True)
    class Meta:
        indexes = (
            (('lat', 'lon', 'dev'), True),
        )

#отметка добавления - для отлова ботов по скорости
class TimePoint(BaseModel):
    time = DateTimeField(default = datetime.datetime.now)
    author = ForeignKeyField(User, backref='activity')

#связь Пользователь-"подтвердил"-Камеру
class UCcheck(BaseModel):
    user = ForeignKeyField(User, backref = 'checked_for')
    camera = ForeignKeyField(Camera, backref = 'checked_by')
    class Meta:
        primary_key = CompositeKey('user', 'camera')

class UReport(BaseModel):
    user = ForeignKeyField(User, backref = 'reported_for')
    camera = ForeignKeyField(Camera, backref = 'reported_by')
    type = SmallIntegerField()
    text = TextField(null = True)
    class Meta:
        primary_key = CompositeKey('user', 'camera')

#связь Админ-проголосовал за Пользователя - добавление админов большинством голосов
class AUvote(BaseModel):
    user = ForeignKeyField(User)
    admin = ForeignKeyField(User)
    class Meta:
        primary_key = CompositeKey('user', 'admin')

#Для обмена сообщениями между админами
class AMessage(BaseModel):
    author = ForeignKeyField(User)
    message = TextField()
    mes_time = DateTimeField(default = datetime.datetime.now)


#если существуют, тихо идем дальше
with db:
    db.create_tables([User, Camera, TimePoint, UCcheck, AUvote, AMessage])
