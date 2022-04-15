from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import requests
import pandas as pd
import numpy as np
import json

from prepare_data import GET_LINK, GET_FLAGURL, GET_CAPITAL, GET_INFO, GET_DIRECTOR, GET_MAP, PROCESSING, SCRAPING_PROCESS, read_data

app = FastAPI()

origins = [
    *
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(background_task: BackgroundTasks):
    data = read_data()
    background_task.add_task(SCRAPING_PROCESS)
    return data


@app.get("/{country}")
async def search(country):
    with open("./database/data.json", encoding='utf-8') as f:
        input_dict = json.load(f)
    # Filter python objects with list comprehensions
    output_dict = [x for x in input_dict if x['name'].lower() ==
                   country.lower()]

    # Transform python object back into json
    output_json = json.dumps(output_dict)
    parsed = json.loads(output_json)

    return parsed
