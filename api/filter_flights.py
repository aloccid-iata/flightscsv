import pandas as pd
 
# Function to filter large CSV in chunks
def filter_large_csv(file_path, origin, destination, date, chunk_size=10000):
    filtered_data = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Apply filter
        filtered_chunk = chunk[(chunk['from_airport_code'] == origin) & 
                               (chunk['dest_airport_code'] == destination) & 
                               (chunk['departure_time'].str.startswith(date))]
        filtered_data.append(filtered_chunk)
    # Concatenate all filtered chunks
    result = pd.concat(filtered_data, ignore_index=True)
    return result.to_dict(orient='records')
 
def handler(event, context):
    origin = event['query']['origin']
    destination = event['query']['destination']
    date = event['query']['date']
    # Specify path to the large CSV file
    file_path = 'flights_with_freight_capacity.csv'  # Replace with your actual file path
    # Filter the data
    filtered_data = filter_large_csv(file_path, origin, destination, date)
    return {
        "statusCode": 200,
        "body": filtered_data
    }
