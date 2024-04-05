# Bluesheets Warehouse API

This project implements a FastAPI-based API for managing warehouse data and running analytics queries on it. It allows users to import line item information from JSON files, store it in a PostgreSQL database, and perform analytics queries such as calculating the total amount spent on specific items.

## Features

- Import line item information from JSON files into the database.
- Calculate the total amount spent on items based on item tags or descriptions.
- Docker-compose setup for easy deployment.
- Prisma ORM for database management.

## Prerequisites

- Docker
- Docker-compose
- Python 3.12

## Installation

1. Clone the repository:

   ```bash
   git clone <...> bluesheets-warehouse-api
   ```

2. Navigate to the project directory:

   ```bash
   cd bluesheets-warehouse-api
   ```

3. Build and run the Docker containers:

   ```bash
   docker compose up -d
   ```

4. Access the API at `http://localhost:8888`.

## Usage

### Local Setup

The use of tools requires running commands locally instead of through Docker. Follow these steps for local setup:

1. Create Python Virtual Environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the Virtual Environment:

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```powershell
     venv\Scripts\activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:

   ```bash
   cp .env.local .env
   ```

5. Prisma generate:

   ```bash
   prisma generate --schema=src/prisma/schema.prisma
   ```

### Importing Data

[Local setup](#local-setup) is required for this section.

To import line item information from JSON files, place your JSON files in a folder and run the import script with the folder path as an argument:

```
python tools/import.py /path/to/data/folder
```

For example,

```bash
python tools/import.py "data"
```

This will import all valid json files found in the root/data.\
See [Behavior](#behavior) for more information.

### Running Analytics Queries

#### Total Spent on Item by Tag

To get the total amount spent on an item by its tag, make a GET request to:

```
http://localhost:8888/total_spent_on_item_by_tag?item_tag=ITEM_TAG
```

Replace `ITEM_TAG` with the tag of the item you want to query.

#### Total Spent on Item by Description

To get the total amount spent on an item by its description, make a GET request to:

```
http://localhost:8888/total_spent_on_item_by_desc?item_desc=ITEM_DESCRIPTION
```

Replace `ITEM_DESCRIPTION` with the description of the item you want to query.

## Configuration

The database connection details can be configured using environment variables. Modify the `.env` file as needed.

## Behavior

### Valid JSON Format

- The import script expects the input data files to be in valid JSON format.
- Each JSON file should contain a `header` array and a `rows` array.
- The `header` array should contain objects representing column headers, each with a `name` and an `id`.
- The `rows` array should contain objects representing data rows, where each object's keys correspond to the `id` values specified in the `header`.

### Valid Headers and Required Columns

- The import script uses a predefined `header_mapping` dictionary to map specific column headers to corresponding fields in the database model.
- If a column header is not found in the `header_mapping`, it will be skipped during import.
- Certain columns may be required for successful import. For example:
  - The `itemTag` column is typically required as it serves as the primary identifier for items.
  - Other columns such as `quantity`, `unitPrice`, and `total` may be required based on the application's business logic.

### Data Transformation and Validation

- During the import process, certain data transformations and validations are applied:
  - Numeric values are converted to float using the `convert_to_float` function.
  - If a value cannot be converted to float, it is set to `None`.
  - Additional header transforms may be applied based on the `header_transforms` dictionary.
  - Null or empty values are filtered out before creating database entries.

### File Import and Database Population

- The import script iterates over each JSON file in the specified folder.
- For each file:
  - It checks if the file has already been imported by querying the `ImportedFile` model in the database.
  - If the file has not been imported:
    - It parses the JSON file and extracts the relevant data.
    - It validates the schema of the data against the predefined `header_mapping`.
    - If the schema is valid, it iterates over each row, transforms and validates the data, and creates database entries using the `Item` model.
    - Finally, it creates an entry in the `ImportedFile` model to mark the file as imported.

This behavior ensures that only valid JSON data with the required headers and columns is imported into the database, while applying necessary transformations and validations during the process.
