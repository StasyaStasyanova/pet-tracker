from peewee import *
import datetime
from ..database import BaseModel
class Pet(BaseModel):
    name = CharField()
    birthday = DateTimeField()
    AnimalType = CharField()
    image = CharField()