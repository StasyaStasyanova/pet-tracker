from peewee import *
from utils import DATA_DIR

DB_FILE = DATA_DIR / "pet-tracker.db"

db = SqliteDatabase(DB_FILE, pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db
        
def init_db():
    from modules.models.pet import Pet
    from modules.models.note import Note
    
    db.connect()
    db.create_tables([Pet, Note], safe=True)
    db.close()