import pandas as pd

# Variables for file paths and column names
file1_path = 'dataset_storm/bug_id_file_mapping.csv'  # Change this
file2_path = 'dataset_storm/storm_metric.csv'  # Change this
output_path = 'dataset_storm/final_storm.csv'  # Path for the output file

bug_file_column = 'File_Name'  # Column name for File_Name in the first CSV
name_file_column = 'Name'  # Column name for Name in the second CSV

# Read the CSV files
file1 = pd.read_csv(file1_path)
file2 = pd.read_csv(file2_path)

# Extract file names from the 'File_Name' column in File 1
file1['Extracted_File_Name'] = file1['File_Name'].str.extract(r'([^/]+\.java)$')

# Create a new column 'Match' in File 2 with default value 'No'
file2['Match'] = 'No'

# Check for matches and update the 'Match' column in File 2
file2.loc[file2['Name'].isin(file1['Extracted_File_Name']), 'Match'] = 'Yes'

# Count the number of 'Yes' matches
yes_count = file2['Match'].value_counts().get('Yes', 0)

# Save the result to a new CSV file
file2.to_csv(output_path, index=False)

# Print the number of matches
print(f"Updated file saved to {output_path}")
print(f"Number of matches (Yes): {yes_count}")
