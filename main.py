from fastapi import FastAPI
import json

def read_data():
    with open("./database/data.json",encoding='utf-8') as f:
        data = json.load(f)
    return data

    

app = FastAPI()

@app.get("/")
async def root():
    data = read_data()
    return data

@app.get("/{id}")
async def search(id):
    with open("./database/data.json",encoding='utf-8') as f:
        input_dict = json.load(f)
    # Filter python objects with list comprehensions
    output_dict = [x for x in input_dict if x['name'] == id]
    
    if(len(output_dict) == 0):
        return {"errors":"please ! try correct country name "}
    
    # Transform python object back into json
    output_json = json.dumps(output_dict)
    parsed = json.loads(output_json)
    
    return parsed