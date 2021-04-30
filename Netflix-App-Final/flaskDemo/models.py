from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_ShowID):
    return entertainment.query.get(int(user_ShowID))
 
class entertainment(db.Model):
    __table__ = db.Model.metadata.tables['entertainment']
class entertainmentcast(db.Model):
    __table__ = db.Model.metadata.tables['entertainmentcast']
class entertainmentcountry(db.Model):
    __table__ = db.Model.metadata.tables['entertainmentcountry']
class entertainmentgenre(db.Model):
    __table__ = db.Model.metadata.tables['entertainmentgenre']
class entertainmentdirector(db.Model):
    __table__ = db.Model.metadata.tables['entertainmentdirector']
class producedin(db.Model):
    __table__ = db.Model.metadata.tables['producedin']
    
 # used for query_factory
def getentertainmentgenre(columns=None):
    u = entertainmentgenre.query
    if columns:
        u = u.options(orm.load_only(*columns))
    return u

def getentertainmentgenreFactory(columns=None):
    return partial(getentertainmentgenre, columns=columns)

    

    

  
