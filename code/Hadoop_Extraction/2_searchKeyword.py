import pandas as pd
import numpy as np

count = 0

def search_algorithm(input_file, output_file):
    df = pd.read_csv(input_file)

    bug_reports = df[['Bug_ID','Bug_Summary','Bug_Description']]

    aging_keywords = [
        'race', 'leak', 'memory', 'aging', 'overflow', 'deplet', 
        'Overflow', 'NPE', 'null pointer', 'Buffer exhausted', 
        'deadlock', 'flush', 'Leak', 'Memory', 'LEAK', 
        'MEMORY', 'OVERFLOW', 'null pointer exception'
    ]

    aging_related_bugs = bug_reports[
        bug_reports['Bug_Summary'].str.contains('|'.join(aging_keywords),case=False, na=False)
        
    ]

    
    aging_related_bugs.drop_duplicates

    print(aging_related_bugs.shape[0])

    aging_related_bugs.to_csv(output_file, index=False)

input_file = 'datasets/hadoop_closed.csv'
output_file = 'datasets/hadoop_ARBIssues.csv'


search_algorithm(input_file,output_file)

