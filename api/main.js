const express = require('express');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const PORT = process.env.PORT || 3000;
const CSV_FILE_PATH = path.join(__dirname, '..', 'flights_with_freight_capacity.csv');

function filterCSV(filePath, origin, destination, date, callback) {
    const results = [];

    fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (data) => {
            if (
                data.from_airport_code === origin &&
                data.dest_airport_code === destination &&
                data.departure_time.startsWith(date)
            ) {
                results.push(data);
            }
        })
        .on('end', () => {
            callback(null, results);
        })
        .on('error', (err) => {
            callback(err, null);
        });
}

app.get('/api/filter', (req, res) => {
    const { origin, destination, date } = req.query;

    if (!origin || !destination || !date) {
        return res.status(400).json({ error: 'Missing query parameters' });
    }

    filterCSV(CSV_FILE_PATH, origin, destination, date, (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to process CSV file' });
        }
        res.status(200).json(results);
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});