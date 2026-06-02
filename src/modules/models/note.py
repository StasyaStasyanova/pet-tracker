import datetime
from peewee import *
from modules.database import BaseModel
from modules.models.pet import Pet

class Note(BaseModel):
    content = TextField(null=True)
    overall_wellbeing = IntegerField(default=3)
    energy = CharField(max_length=50, null=True)
    appetite = CharField(max_length=50, null=True)
    mood = CharField(max_length=50, null=True)
    activity = CharField(max_length=50, null=True)
    pet = ForeignKeyField(Pet, backref='notes', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)