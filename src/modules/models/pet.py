from peewee import *
import datetime
from ..database import BaseModel
class Pet(BaseModel):
    name = CharField()
    birthday = DateTimeField()
    age = IntegerField()
    AnimalType = CharField()
    image = CharField()