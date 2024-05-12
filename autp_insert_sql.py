import pyperclip
import csv
import os

def is_digit(value):
  if isinstance(value, str):
    return value.isdigit()
  try:
    int(value)
    return True
  except ValueError:
    return False

def join_data(statement,data):
  result = statement
  for inner_list in data:
    inner_list_str = [str(x) if is_digit(x) else "'" + str(x) + "'" for x in inner_list]
    result = result +"\n(" + ", ".join(inner_list_str) + "),"
  return result

def convert_csv_to_list(filename):
  data = []
  with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      data.append(list(row))
  return data

def take_input():
  table = input("Enter table name: ")
  data = convert_csv_to_list(f"{os.path.dirname(__file__)}\data.csv")
  return table, data

table, data = take_input()
result = join_data(f"INSERT INTO {table} VALUES ",data)
result = result[:-1] + ";"
pyperclip.copy(result)
print(result)