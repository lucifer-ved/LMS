from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)

def commit_to_db(obj,type):
    try:
        if type  == 'add' or type == 'update': 
            db.session.add(obj)
        if type == 'bulkadd': 
            db.session.bulk_save_objects(obj)
        if type == 'delete': 
            obj.delete()
        db.session.commit()
    except Exception as e:
        print(e)