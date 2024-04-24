# Goal Play arround with extracting text form a pdf file

# Importing the required libraries
from PyPDF2 import PdfReader
import pandas as pd

# Function to extract text from a pdf file
def extract_text_from_pdf(pdf_path):
    # Open the pdf file
    with open(pdf_path, "rb") as file:
        # Create a pdf reader object
        pdf = PdfReader(file)
        # Initialize a variable to store the text
        text = ""
        # Loop through the pages of the pdf file
        for page in range(len(pdf.pages)):
            # Extract the text from the page
            text += pdf.pages[page].extract_text()
        # Return the extracted text
    return text

# Path to the pdf file
pdf_path = "112723 WellsFargo.pdf"

# Extract text from the pdf file
text = extract_text_from_pdf(pdf_path)

# Print the extracted text
# print(text)

# Search for all occurances of the phrase 
search_phrase = "Purchases, Balance Transfers & Other Charges"
search_len = len(search_phrase)+1

# Only print the text after the search phrase
index = text.find(search_phrase)
#print(text[index+search_len:])

# Read the 4 digits form the line after the search phrase
digits = text[index+search_len:index+search_len+4]
# print(digits)

# Only print each line after the search phrase that shares the exact same 4 starting characters
lines = text[index+search_len:].split("\n")
expense_list = []

for line in lines:
    if line[:4] == digits:
        expense_list.append(line)
        print(line)

# Print the list of expenses
#print(expense_list)

# Create an empty DataFrame
#"4 Digits","Date1", "Date2", "id" ,"Description", "Amount"
df = pd.DataFrame({
    "4 Digits": [],
    "Date1": [],
    "Date2": [],
    "id": [],
    "Description": [],
    "Amount": []
})


# show the content of the DataFrame
# print(df)
# print(df.dtypes)

df = df.astype(object)

for expense in expense_list:
    # Extract the id from the line
    id = " ".join(expense.split(" ")[1:3])
    # Write to the DataFrame
    df.loc[df.index.max() + 1] = {"id": id}

    # Extract the 4 digits from the line
    four_digits = expense[:4]
    # Write to the DataFrame
    df.loc[df["id"] == id, "4 Digits"] = four_digits

    # Extract the date 1 from the line
    date1 = expense.split(" ")[1][:5]
    # Write to the DataFrame
    df.loc[df["id"] == id, "Date1"] = date1

    # Extract the date 2 from the line
    date2 = expense.split(" ")[1][5:10]
    # Write to the DataFrame
    df.loc[df["id"] == id, "Date2"] = date2

    # Extract the description from the line
    description = " ".join(expense.split(" ")[3:])
    # Write to the DataFrame
    df.loc[df["id"] == id, "Description"] = description

    # Extract the amount from the line
    amount = expense.split(" ")[-1]
    # remove the ammount form the end of the string
    description = description[:-len(amount)]

    # Write to the DataFrame
    df.loc[df["id"] == id, "Amount"] = amount


df['4 Digits'] = df['4 Digits'].astype(int)
df['Date1'] = df['Date1'].astype(str)
df['Date2'] = df['Date2'].astype(str)
df['id'] = df['id'].astype(str)
df['Description'] = df['Description'].astype(str)
df['Amount'] = df['Amount'].astype(float)


# Print the DataFrame
print("##################################")
print(df)







