from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, FastAPI

MYSQL_USER = 'root'
MYSQL_PASSWORD = ""
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'fastapidatabase'

DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()

class Task(Base):
    __tablename__ = "myinfotable"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastdate = Column(Text)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/")
def create_task(id:int , name: str, lastdate: str, db: Session = Depends(get_db)):
    new_task = Task(id=id , name=name , lastdate=lastdate)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/gettasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("newmain:app", host="127.0.0.1", port=8000, reload=True)