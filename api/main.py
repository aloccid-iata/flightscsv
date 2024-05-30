from fastapi import FastAPI, Query
from .filter import filter_large_csv  # Note the relative import

app = FastAPI()

@app.get("/filter")
async def filter_handler(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    date: str = Query(..., description="Departure date")
):
    # Specify path to the large CSV file
    file_path = 'flights_with_freight_capacity.csv'
    
    # Filter the data
    filtered_data = filter_large_csv(file_path, origin, destination, date)
    return {
        "statusCode": 200,
        "body": filtered_data
    }
