# ZVV Data Analysis

This project analyzes public transportation data from the Zürcher Verkehrsverbund (ZVV) and Verkehrsbetriebe Zürich (VBZ). The data is sourced from opendata.swiss.

## Datasets

The project uses the following datasets:

- Passenger count data from 2018 to 2023
- VBZ infrastructure data

## Scripts

- `vbz_examples/example_passengerdata.py`: Demonstrates how to work with passenger data, including loading, merging, and analyzing passenger counts per line and stop.
- `vbz_examples/example_traveltimedata.py`: Demonstrates how to work with travel time data to calculate punctuality per line.
- `top25_stations_2023/app.py`: Visualizes the top 25 most used stations based on passenger data from 2023.

## Data Sources

[Datasets from opendata.swiss](https://opendata.swiss/de/dataset/fahrgastzahlen-vbz1)

- [vbz-infrastruktur](https://opendata.swiss/de/dataset/vbz-infrastruktur-ogd)
