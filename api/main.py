from fastapi import FastAPI, Request
from filter import filter_large_csv

app = FastAPI()

@app.post("/filter")
async def filter_handler(request: Request):
    data = await request.json()
    origin = data['query']['origin']
    destination = data['query']['destination']
    date = data['query']['date']
    
    # Specify path to the large CSV file
    file_path = 'flights_with_freight_capacity.csv'
    
    # Filter the data
    filtered_data = filter_large_csv(file_path, origin, destination, date)
    return {
        "statusCode": 200,
        "body": filtered_data
    }
