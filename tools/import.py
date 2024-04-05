import json
import os
import sys

from prisma import Prisma
from prisma.models import Item
from prisma.models import ImportedFile

db = Prisma(auto_register=True)

def convert_to_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

header_mapping = {
    "S/N": None,  # Skip this header
    "CODE": "itemTag",
    "ITEM": "itemTag",
    "ITEM#": "itemTag",
    "ITEM NO": "itemTag",
    "ITEM NO.": "itemTag",
    "ITEM CODE": "itemTag",
    "ITEM ID": "itemTag",
    "PRODUCT CODE": "itemTag",
    "MATERIAL NO": "itemTag",
    "MATERIAL": "itemTag",
    "STOCK CODE": "itemTag",
    
    "ITEM DESCRIPTION": "description",
    "DESCRIPTION": "description",
    
    "QTY": "quantity",
    "SUPPLIED": "quantity",
    "QUANTITY": "quantity",
    
    "UNIT PRICE": "unitPrice",
    "UNITPRICE": "unitPrice",
    "U/PRICE": "unitPrice",
    
    "AMOUNT": "total",
    "TOTAL": "total",
    "TOTAL AMOUNT": "total",
    
    "TAX": "tax",
    
    "DISC.": "discount",
    
    "UOM": "unitOfMeasure",
    "UNIT": "unitOfMeasure",
    
    "PKG": "packageNumber",
    "PKG#": "packageNumber",
    
    "DISC": "discount",
}

header_transforms = {
    "quantity": lambda x: convert_to_float(x),
    "unitPrice": lambda x: convert_to_float(x),
    "total": lambda x: convert_to_float(x),
    "tax": lambda x: convert_to_float(x),
}

async def setup():
    await db.connect()

async def import_data_files(folder_path):
    files = os.listdir(folder_path)
    total_files_len = len(files)
    
    for i in range(len(files)):
        if i % 250 == 0:
            print(f"Importing file {i+1}/{total_files_len}")
        file_name = files[i]
            
        # Check if file has already been imported
        existing_file = await ImportedFile.prisma().find_first(where={'fileName': file_name})
                
        if not existing_file:
            # File has not been imported, import it and create entry in ImportedFile model
            if await insert_items_from_json(os.path.join(folder_path, file_name)):
                await ImportedFile.prisma().create(data={'fileName': file_name})


async def insert_items_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        
    if not "header" in data or not "rows" in data:
        return
    
    headers = data.get('header', [])
    schema_fields = []
    schema_to_header_map = {}
    valid_schema = False
    
    for header in headers:
        headerName = header['name'].upper()
        if headerName in header_mapping:
            schema_field = header_mapping[headerName]
            if schema_field:
                schema_fields.append(schema_field)
                schema_to_header_map[schema_field] = header['id']
                
                if schema_field == "itemTag":
                    valid_schema = True
                
    if not valid_schema:
        return
    
    for row in data['rows']:
        item_data = {}
        
        for schema_field in schema_fields:
            headerName = schema_to_header_map[schema_field]
            value = row.get(headerName, {}).get('value')
            if value:
                transformed_value = header_transforms[schema_field](value) if schema_field in header_transforms else value
                item_data[schema_field] = transformed_value
        
        item_data = {key: value for key, value in item_data.items() if value is not None}
        if "itemTag" not in item_data:
            continue
        await Item.prisma().create(data=item_data)
        
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python tools/import.py <data_folder_path>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    loop.run_until_complete(import_data_files(folder_path))
    loop.close()