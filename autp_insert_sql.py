import pyperclip
import csv
import os

def is_digit(value):
    """
    Checks if a value is an integer or a string containing only digits.
    """
    if isinstance(value, str):
        return value.isdigit()
    try:
        int(value)
        return True
    except ValueError:
        return False

def join_data(sql_statement, data_list):
    """
    Joins a list of lists to a SQL statement.

    The function takes an empty SQL statement and a list of lists as input.
    It returns a string representing the SQL statement with the data
    from the list of lists joined to it.

    Args:
        sql_statement: The SQL statement to join the data to.
        data_list: The list of lists to join to the SQL statement.

    Returns:
        A string representing the SQL statement with the data joined to it.
    """
    joined_data = ""
    for data in data_list:
        # Format each element in the inner list as a string.
        # If the element is an integer, leave it as is, otherwise wrap it in single quotes.
        data_str = [str(x) if is_digit(x) else "'{}'".format(x) for x in data]
        # Add the inner list as a row in the SQL statement, separated by commas.
        joined_data += "({}),".format(", ".join(data_str))
    # Remove the trailing comma and add a semicolon to the end of the statement.
    return sql_statement + joined_data[:-1] + ";"



def convert_csv_to_list(filename):
    """
    Converts a CSV file to a list of lists.

    The function takes a filename as input and returns a list of lists, where each
    inner list corresponds to a row in the CSV file and each element in the inner list
    corresponds to a cell in that row.

    The function raises a ValueError if the input file does not exist or is not a CSV file.

    Args:
        filename: The name of the CSV file to read

    Returns:
        A list of lists, where each inner list is a row in the CSV file
    """
    # Check that the input file exists and is a CSV file
    if not os.path.isfile(filename):
        raise ValueError(f"{filename} does not exist or is not a file")
    if not filename.lower().endswith(".csv"):
        raise ValueError(f"{filename} is not a CSV file")

    data = []
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)  # Read the CSV file
            for row in reader:  # Loop over the rows in the CSV file
                data.append(list(row))  # Add the row to the output data
    except csv.Error:
        raise ValueError(f"{filename} is not a valid CSV file")
    return data  # Return the data



def take_input():
  table = input("Enter table name: ")
  data = convert_csv_to_list(f"{os.path.dirname(__file__)}\data.csv")
  return table, data

table, data = take_input()
result = join_data(f"INSERT INTO {table} VALUES ",data)
pyperclip.copy(result)
print(result)