from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABSE_URL='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' #connection string

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)                   #responsible for sqlalchemy to connect to Postgres database
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base= declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
#SQLALCHEMY_DATABSE_URL='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' #connection string
"""A sessionmaker is a factory function for creating new Session objects. In this line:

autocommit=False specifies that changes made within a session should not be automatically committed 
to the database. This allows us to manually control when to commit changes.

autoflush=False disables autoflush behavior, meaning SQLAlchemy won't automatically issue SQL queries 
to synchronize the state of objects with the database.

bind=engine binds the sessionmaker to the engine we created earlier, meaning any sessions created by this 
sessionmaker will use the specified engine to connect to the database."""