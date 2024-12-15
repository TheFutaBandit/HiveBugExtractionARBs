from jira import JIRA
import csv

jira = JIRA(server="https://issues.apache.org/jira")

counter = 0
total_results = 0
batch_size = 1000  # Set the batch size to 1000

csv_file_name = "dataset_storm/storm_closed.csv"

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Bug_ID", "Bug_Summary", "Bug_Description"])

    start_at = 0
    while True:
        issues = jira.search_issues(
            "project = STORM and status = closed", 
            startAt=start_at, 
            maxResults=batch_size
        )

        if not issues:
            break  # Exit loop if no more issues are returned

        total_results += len(issues)

        for issue in issues:
            bug_id = issue.key
            bug_summary = issue.fields.summary
            bug_description = issue.fields.description
            counter += 1
            writer.writerow([bug_id, bug_summary, bug_description])

        start_at += batch_size

print(f"Data export successful with {total_results} results")
