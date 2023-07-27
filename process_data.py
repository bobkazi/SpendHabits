# Import necessary libraries
import pandas as pd
import sqlite3

# Load the original data again
data = pd.read_excel("statement data.xlsx")

# Define the regular expressions for the date, amount, balance and bank_charges
date_regex = r"(\d{2} \w{3})"
amount_regex = r"((?:\d{1,3},)*\d{1,3}\.\d{2}(?:Cr)?)"
balance_regex = r"((?:\d{1,3},)*\d{1,3}\.\d{2}Cr(?: \d{1,3}\.\d{2})?)"
bank_charges_regex = r"(?<=Cr )(\d{1,3}\.\d{2})?"

# Apply the regular expressions to extract the date, amount, balance and bank_charges
data["Date"] = data["Unnamed: 0"].str.extract(date_regex, expand=False)
data["Amount"] = data["Unnamed: 0"].str.extract(amount_regex, expand=False)
data["Balance"] = data["Unnamed: 0"].str.extract(balance_regex, expand=False)
data["Bank_charges"] = data["Unnamed: 0"].str.extract(bank_charges_regex, expand=False)

# Remove the extracted fields from the original text
data["Remaining_text"] = data["Unnamed: 0"].str.replace(date_regex, "").str.replace(amount_regex, "").str.replace(balance_regex, "").str.replace(bank_charges_regex, "", regex=True)

# Split the remaining text into description and reference based on the first occurrence of a digit followed by a non-digit
split_text = data["Remaining_text"].str.split(r"(\d[^0-9].*)", 1, expand=True)

# Assign the split text to the "Description" and "Reference" columns
data["Description"] = split_text[0]
data["Reference"] = split_text[1]

# Let's drop the columns we no longer need and reorder the remaining ones
processed_data = data[['Date', 'Description', 'Reference', 'Amount', 'Balance', 'Bank_charges']]

# Connect to the SQLite database
# If the database does not exist, it will be created
conn = sqlite3.connect('statement_data.db')

# Write the data to the database
processed_data.to_sql('Statement', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
