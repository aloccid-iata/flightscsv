import pandas as pd

def filter_large_csv(file_path, origin, destination, date, chunk_size=10000):
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
