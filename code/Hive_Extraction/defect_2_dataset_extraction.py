import pandas as pd
import numpy as np

def search_algorithm(input_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Select relevant columns
    bug_reports = df[['Bug_ID', 'Bug_Summary', 'Bug_Description']]

    # List of aging-related keywords
    aging_keywords = [
        'race', 'leak', 'memory', 'aging', 'overflow', 'deplet', 
        'Overflow', 'NPE', 'null pointer', 'Buffer exhausted', 
        'deadlock', 'flush', 'Leak', 'Memory', 'LEAK', 
        'MEMORY', 'OVERFLOW', 'null pointer exception'
    ]

    # Create a boolean column indicating if any aging-related keyword is present
    bug_reports['Is_Aging_Related'] = bug_reports['Bug_Summary'].str.contains(
        '|'.join(aging_keywords), case=False, na=False
    )

    # Add a 'Yes/No' column based on the boolean values
    bug_reports['Aging_Related'] = bug_reports['Is_Aging_Related'].apply(lambda x: 'Yes' if x else 'No')

    # Drop the intermediate boolean column
    bug_reports.drop(columns=['Is_Aging_Related'], inplace=True)

    # Save the result to the output file
    bug_reports.to_csv(output_file, index=False)

    # Print the count of aging-related bugs
    print(f"Aging-related issues: {bug_reports['Aging_Related'].value_counts()['Yes']}")

# File paths
input_file = 'datasets/HIVE_Closed.csv'
output_file = 'Defect_Dataset/HIVE_ISSUES_Classification.csv'

# Execute the function
search_algorithm(input_file, output_file)
