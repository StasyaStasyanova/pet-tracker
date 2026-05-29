from peewee import *
from modules.database import BaseModel
class Pet(BaseModel):
    name = CharField()
    birthday = DateTimeField()
    AnimalType = CharField()
    image = CharField()