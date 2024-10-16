import pandas as pd

# Variables for file paths and column names
bug_file_path = 'datasets/bug_id_file_mapping.csv'  # Path to the file containing Bug_ID and File_Name
name_file_path = 'datasets/Hive_metrics.csv'  # Path to the file containing the Name column
output_file_path = 'datasets/ARB_Hive_Metric.csv'  # Path for the output file

bug_file_column = 'File_Name'  # Column name for File_Name in the first CSV
name_file_column = 'Name'  # Column name for Name in the second CSV

# Load the first CSV with columns [Bug_ID, File_Name]
bug_file = pd.read_csv(bug_file_path)

# Load the second CSV that contains the column 'Name'
name_file = pd.read_csv(name_file_path)

# Extract actual file names from 'File_Name' (after the last '/')
bug_file['Extracted_File_Name'] = bug_file[bug_file_column].apply(lambda x: x.split('/')[-1])

# Extract actual names from 'Name' (after the last '.')
name_file['Extracted_Name'] = name_file[name_file_column].apply(lambda x: x.split('.')[-1])

# Create a set of unique extracted file names for matching
bug_names_set = set(bug_file['Extracted_File_Name'])

# Create a new column 'Matched' in the name_file which is 'Yes' if there's a match, otherwise 'No'
name_file['Matched'] = name_file['Extracted_Name'].apply(lambda x: 'Yes' if x in bug_names_set else 'No')

# Drop the helper 'Extracted_Name' column
name_file.drop(columns=['Extracted_Name'], inplace=True)

# Save the modified DataFrame to a new CSV
name_file.to_csv(output_file_path, index=False)

print(f"Output file with matched column has been saved as '{output_file_path}'")
