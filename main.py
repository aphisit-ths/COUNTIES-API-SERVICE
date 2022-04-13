from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json

def read_data():
    with open("./database/data.json",encoding='utf-8') as f:
        data = json.load(f)
    return data

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    data = read_data()
    return data

@app.get("/{country}")
async def search(country):
    with open("./database/data.json",encoding='utf-8') as f:
        input_dict = json.load(f)
    # Filter python objects with list comprehensions
    output_dict = [x for x in input_dict if x['name'].lower() == country.lower()]
    
    # Transform python object back into json
    output_json = json.dumps(output_dict)
    parsed = json.loads(output_json)
        
    return parsed