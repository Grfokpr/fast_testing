from decouple import config
import ctypes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn
import hashlib
import resource

DATABASE_URL = config('DATABASE_URL')

app = FastAPI()


# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()


# class Number(Base):
#     __tablename__ = "numbers"
#
#     id = Column(Integer, primary_key=True, index=True)
#     num1 = Column(Float)
#     num2 = Column(Float)
#     result = Column(Float)
#
#
# Base.metadata.create_all(bind=engine)
#
#
# class Numbers(BaseModel):
#     num1: float
#     num2: float


@app.get("/")
def add_numbers():
    return {"result": 'YEEEH'}

# @app.post("/add")
# def add_numbers(numbers: Numbers):
#     result = numbers.num1 + numbers.num2
#
#     db = SessionLocal()
#     db_number = Number(num1=numbers.num1, num2=numbers.num2, result=result)
#     db.add(db_number)
#     db.commit()
#     db.refresh(db_number)
#     db.close()
#
#     return {"result": result}

def emulate_cpu_usage(milliseconds):
    target_cpu_time = milliseconds / 1000  # Convert milliseconds to seconds
    rusage_start = resource.getrusage(resource.RUSAGE_SELF)

    while True:
        # Create a hash using a CPU-intensive operation.
        h = hashlib.md5()
        h.update(b"data_to_hash")
        _ = h.hexdigest()

        rusage_stop = resource.getrusage(resource.RUSAGE_SELF)
        user_time = (
            (rusage_stop.ru_utime - rusage_start.ru_utime) +
            (rusage_stop.ru_stime - rusage_start.ru_stime)
        )

        if user_time >= target_cpu_time:
            break

    total_cpu_time = user_time
    return total_cpu_time

def usleep(microseconds):
    _libc = ctypes.CDLL(None)
    _libc.usleep(microseconds)

async def emulate_io_usage(milliseconds):
    usleep(milliseconds * 1000)  # Convert milliseconds to microseconds
    return milliseconds / 1000  # Return the duration of I/O emulation

@app.get("/emulate")
async def emulate(cpu_milliseconds: int = 0, io_milliseconds: int = 0):
    if cpu_milliseconds > 0:
        cpu_time = emulate_cpu_usage(cpu_milliseconds)
    else:
        cpu_time = 0.0

    if io_milliseconds > 0:
        io_time = await emulate_io_usage(io_milliseconds)
    else:
        io_time = 0.0

    return {"done": "done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
