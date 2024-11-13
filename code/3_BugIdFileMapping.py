import pandas as pd
import subprocess
import os

# Step 1: Load Bug IDs from CSV
def load_bug_ids(csv_file):
    df = pd.read_csv(csv_file)
    return df['Bug_ID'].tolist()  # Adjust the column name if necessary

# Step 2: Search for Bug IDs in Commit Messages and Collect File Names
def search_bug_ids(bug_ids, repo_dir):
    os.chdir(repo_dir)  # Change to the directory of the cloned repository
    results = []  # List to store results

    for bug_id in bug_ids:
        print(f"\nSearching for Bug ID: {bug_id}")
        result = subprocess.run(['git', 'log', '--grep={}'.format(bug_id), '--name-only'], capture_output=True, text=True)
        
        if result.stdout:
            # Split the output into lines and filter out empty lines
            lines = result.stdout.strip().split('\n')
            # The last line will be empty due to '--name-only', so we ignore it
            files = [line for line in lines if line and not line.startswith('commit')]
            for file in files:
                results.append({'Bug_ID': bug_id, 'File_Name': file})  # Append bug ID and file name to results
        else:
            print(f"No commits found for Bug ID {bug_id}.")

    return results

# Main Function
def main():
    # Configuration
    csv_file = 'dataset_storm/storm_ARBIssues.csv'  # Path to your CSV file containing bug IDs
    repo_dir = '../stormSoftware/storm'  # Path to your cloned Apache Hive repository
    output_csv = 'bug_id_file_mapping.csv'  # Output CSV file path

    # Ensure datasets directory exists (relative to where the script is run)
    os.makedirs('datasets', exist_ok=True)

    # Print current working directory
    print("Current Working Directory:", os.getcwd())

    # Execute Steps
    bug_ids = load_bug_ids(csv_file)
    results = search_bug_ids(bug_ids, repo_dir)

    # Create a DataFrame and save it to a CSV file
    results_df = pd.DataFrame(results)
    
    # Print output CSV path
    print("Output CSV Path:", output_csv)

    results_df.to_csv(output_csv, index=False)

    print(f"\nResults saved to {output_csv}")

if __name__ == "__main__":
    main()