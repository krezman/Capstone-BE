# Dependencies for creating models
from peewee import *
import datetime

from flask_login import UserMixin


DATABASE = SqliteDatabase('yd.sqlite')

# User/Vendor Model
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    vendor_name = CharField()
    vendor_type = IntegerField()
    location = CharField()
    profile_photo = CharField()
    bio = CharField(max_length = 500)

    class Meta:
        database = DATABASE


# Post Model
class Post(Model):
    photo = CharField()
    text = CharField(max_length = 200)
    date_created = DateTimeField(default=datetime.datetime.now)
    post_owner = ForeignKeyField(User, backref='yd')

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User, Post], safe=True)
    print("Connected to the DB AND created tables if they don't already exist!")
    DATABASE.close()