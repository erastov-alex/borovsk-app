from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'database.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# def create_db():
#     Base.metadata.create_all(engine)
    
# def db_check():
#     db_is_created = os.path.exists(DATABASE_NAME)
#     if not db_is_created:
#         create_database()
        
# db_check()       
