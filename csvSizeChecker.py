import csv

file_path = "all.csv"  ## replace this with the path to the csv file

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    num_rows = len(rows)
    num_columns = len(rows[0]) if rows else 0

print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")