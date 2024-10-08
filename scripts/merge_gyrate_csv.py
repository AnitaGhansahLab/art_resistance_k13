import os
import pandas as pd

# Step 1: Create a new DataFrame for the merged data
merged_data = pd.DataFrame(columns=['gyrate (nm)', 'Systems'])

# Step 2: Get the current working directory
current_directory = os.getcwd()

# Step 3: Define the list of CSV files in the desired order
csv_files = [
    'wild_gyrate.csv', 
    'A657V_gyrate.csv', 
    'C580Y_gyrate.csv',
    'M476I_gyrate.csv',
    'P553L_gyrate.csv',
    'P574L_gyrate.csv',
    'R561H_gyrate.csv',
    'A557S_gyrate.csv',
    'A578S_gyrate.csv',
    'Y493H_C580Y_gyrate.csv'
    # Add other CSV file names as needed
]

# Step 4: Loop through each CSV file
for csv_file in csv_files:
    # Construct the absolute path for the CSV file
    full_path = os.path.join(current_directory, csv_file)
    
    # Check if the CSV file exists
    if not os.path.isfile(full_path):
        print(f"File not found: {full_path}. Skipping this file.")
        continue  # Skip to the next file if the current one doesn't exist
    
    # Step 5: Load the current CSV file into a DataFrame, specifying only column A
    print(f"Reading file: {full_path}")  # Print the file being read
    df = pd.read_csv(full_path, usecols=[0], header=None)  # Use column A, no headers
    
    # Step 6: Extract the data from column A, assuming it's in all rows of column 0
    gyrate_data = df.iloc[:, 0].dropna()  # Drop any empty rows
    
    # Step 7: Create a DataFrame with the current data and the system name (CSV file name)
    system_data = pd.DataFrame({
        'gyrate (nm)': gyrate_data,
        'Systems': [os.path.basename(csv_file)] * len(gyrate_data)
    })
    
    # Only concatenate if system_data is not empty
    if not system_data.empty:
        merged_data = pd.concat([merged_data, system_data], ignore_index=True)

# Step 8: Save the final merged DataFrame to a new CSV file
merged_data.to_csv('merged_gyrate_data.csv', index=False)

print("Data merged successfully!")
