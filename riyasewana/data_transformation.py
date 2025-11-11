import time
import pandas as pd
from tqdm import tqdm
import os
import re

# makes = ['honda', 'nissan', 'suzuki', 'micro', 'mitsubishi', 'mahindra', 'mazda', 'daihatsu', 'hyundai', 'kia', 'bmw', 'perodua', 'tata']
# # makes = ['honda','micro']

file_path = os.path.join('scrape_data',"v02",f'extracted_table_data.csv')

dataset = pd.read_csv(file_path)

# Remove records with 'Negotiable' value in the 'Price' column
dataset = dataset[dataset['vehicle_price'] != 'Negotiable']

# Extract only the numerical part of the 'Price' column, ignoring any additional text
def extract_price(price):
    numbers = re.findall(r'\d+', price.replace('Rs. ', '').replace(',', ''))
    return int(numbers[0]) if numbers else None

dataset['vehicle_price'] = dataset['vehicle_price'].apply(extract_price)

# Remove records with None values in the 'Price' column
dataset = dataset.dropna(subset=['vehicle_price'])

# Convert the 'Model' column to uppercase
dataset['model'] = dataset['model'].str.upper()
dataset['brand'] = dataset['brand'].str.upper()
dataset['Transmission'] = dataset['Transmission'].str.upper()
dataset['fuel_type'] = dataset['fuel_type'].str.upper()

output_file_path = os.path.join('transformed_data',"V02",f'transformed_table_data.csv')

dataset.to_csv(output_file_path, index=False)
