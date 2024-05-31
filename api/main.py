from fastapi import FastAPI, Query
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def filter_large_csv(file_path, origin, destination, date, chunk_size=10000):
    logger.info(f"Reading CSV file: {file_path}")

    # Read the entire CSV to log its contents
    df = pd.read_csv(file_path)
    logger.info(f"CSV file loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
    logger.info(f"First few rows of the CSV file:\n{df.head()}")

    filtered_data = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Apply filter
        filtered_chunk = chunk[
            (chunk['from_airport_code'] == origin) & 
            (chunk['dest_airport_code'] == destination) & 
            (chunk['departure_time'].str.startswith(date))
        ]
        filtered_data.append(filtered_chunk)
    # Concatenate all filtered chunks
    result = pd.concat(filtered_data, ignore_index=True)
    return result.to_dict(orient='records')

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
