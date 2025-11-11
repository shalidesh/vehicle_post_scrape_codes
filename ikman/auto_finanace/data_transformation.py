import time
import pandas as pd
from tqdm import tqdm
import os
import re

file_path = os.path.join('data','2025-06-05','auto_finance_post_data.csv')

dataset = pd.read_csv(file_path)

dataset = dataset.dropna()

dataset = dataset[dataset['Brand'] != '0']

# Remove records with 'Negotiable' value in the 'Price' column
dataset = dataset[['Brand','Model','Trim / Edition','Year of Manufacture','Transmission','Body type','Fuel type','Engine capacity','Mileage','Vehicle_Price']]

# Extract only the numerical part of the 'Price' column, ignoring any additional text
def extract_price(price):
    numbers = re.findall(r'\d+', price.replace('Rs. ', '').replace(',', ''))
    return int(numbers[0]) if numbers else None

def extract_engine(engine_cap):
    numbers = re.findall(r'\d+', engine_cap.replace(' cc', '').replace(',', ''))
    return int(numbers[0]) if numbers else None


def extract_milage(milage):
    numbers = re.findall(r'\d+', milage.replace(' km', '').replace(',', ''))
    return int(numbers[0]) if numbers else None

def extract_name(model):
    numbers = re.findall(r'\d+', model.replace('-', ' ').replace(',', ''))
    return int(numbers[0]) if numbers else None

# Function to clean and concatenate model names
def clean_model_name(model_name):
    return model_name.replace("-", "")

# Apply the function to the dataset
dataset['Model'] = dataset['Model'].apply(clean_model_name)
dataset['Vehicle_Price'] = dataset['Vehicle_Price'].apply(extract_price)
dataset['Engine capacity'] = dataset['Engine capacity'].apply(extract_engine)
dataset['Mileage'] = dataset['Mileage'].apply(extract_milage)

# Remove records with None values in the 'Price' column
dataset = dataset.dropna(subset=['Vehicle_Price'])


# Convert the 'Model' column to uppercase
dataset['Model'] = dataset['Model'].astype(str).str.upper()
dataset['Brand'] = dataset['Brand'].astype(str).str.upper()
dataset['Trim / Edition'] = dataset['Trim / Edition'].astype(str).str.upper()
dataset['Year of Manufacture'] = dataset['Year of Manufacture'].astype(str).str.upper()
dataset['Transmission'] = dataset['Transmission'].astype(str).str.upper()
dataset['Body type'] = dataset['Body type'].astype(str).str.upper()
dataset['Fuel type'] = dataset['Fuel type'].astype(str).str.upper()
dataset['Engine capacity'] = dataset['Engine capacity'].astype(str)
dataset['Mileage'] = dataset['Mileage'].astype(str)

dataset.rename(columns={'Model': 'model', 
                        'Brand': 'brand', 
                        'Year of Manufacture':'year',
                        'Fuel type': 'fuel_type', 
                        'transmision': 'transmision', 
                        'engine_capacity': 'engine_capacity', 
                        'Vehicle_Price': 'vehicle_price'}, inplace=True)

output_file_path = os.path.join('data','2025-06-05', f'transformed_table_data.csv')
dataset.to_csv(output_file_path, index=False)

