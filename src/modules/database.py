from peewee import *
from ..utils import DATA_DIR
import os

DB_FILE = os.path.join(DATA_DIR, 'pet-tracker.db')

db = SqliteDatabase(DB_FILE)

class BaseModel(Model):
    class Meta:
        database = db