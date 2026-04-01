from peewee import *
from ..database import BaseModel
from .pet import Pet

class Note(BaseModel):
    content = TextField()
    pet = ForeignKeyField(Pet, backref='notes')