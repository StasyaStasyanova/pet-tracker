from peewee import *
from utils import DATA_DIR
import os
# from modules.models.pet import Pet
# from modules.models.note import Note

DB_FILE = os.path.join(DATA_DIR, 'pet-tracker.db')

db = SqliteDatabase(DB_FILE)

class BaseModel(Model):
    class Meta:
        database = db
        
def init_db():
    from modules.models.pet import Pet
    from modules.models.note import Note
    
    db.connect()
    db.create_tables([Pet, Note], safe=True)
    db.close()