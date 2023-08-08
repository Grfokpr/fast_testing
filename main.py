from decouple import config

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

DATABASE_URL = config('DATABASE_URL')

app = FastAPI()


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Number(Base):
    __tablename__ = "numbers"

    id = Column(Integer, primary_key=True, index=True)
    num1 = Column(Float)
    num2 = Column(Float)
    result = Column(Float)


Base.metadata.create_all(bind=engine)


class Numbers(BaseModel):
    num1: float
    num2: float


@app.post("/add")
def add_numbers(numbers: Numbers):
    result = numbers.num1 + numbers.num2

    db = SessionLocal()
    db_number = Number(num1=numbers.num1, num2=numbers.num2, result=result)
    db.add(db_number)
    db.commit()
    db.refresh(db_number)
    db.close()

    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
