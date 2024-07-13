from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
async def generate_random_number():
    return {"random_number": random.randint(1, 100)}

@app.get("/random/{limit}")
async def generate_random_numbers(limit: int):
    return {"Limit":limit,"random_number": random.randint(1, limit)}