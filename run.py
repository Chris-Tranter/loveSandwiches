import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# All constant variables in python have capital letters!
# SET the scope and list the API's available

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Pulling from the imported gspread we retrieve the service account  using consant variables

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('loveSandwiches')

# Functionality

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True
'''
                                                                # update sales worksheet from user input

                                                                def update_sales_worksheet(data):
                                                                    """
                                                                    Update sales worksheet, in a new row
                                                                    """
                                                                    print("Updating sales worksheet...\n")
                                                                    sales_worksheet = SHEET.worksheet("sales")
                                                                    sales_worksheet.append_row(data)
                                                                    print("Sales worksheet updated successfully.\n")

                                                                # update surplus worksheet from user input

                                                                def update_surplus_worksheet(data):
                                                                    """
                                                                    Update surplus worksheet, in a new row
                                                                    """
                                                                    print("Updating surplus worksheet...\n")
                                                                    surplus_worksheet = SHEET.worksheet("surplus")
                                                                    surplus_worksheet.append_row(data)
                                                                    print("Surplus worksheet updated successfully.\n")
'''
# refactoring the 2 functions used previously to update the worksheet in one function

def update_worksheet(data, worksheet):
    """
    User enters data which updates to the corresponding worksheet
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully \n")



# surplus data calculator parsed with sales data list 

def calculate_surplus_data(sales_row):
    """
    Compares the sales and stock then calculates the surplus data.
    - Positive surplus indicates waste
    - Negative surplus indicates extra sandwiches made.
    """
    print("Calculating surplus data...\n")
    #                           GET ALL VALUES is another method from the gspread library
    stock = SHEET.worksheet("stock").get_all_values()
    #                 -1       pulls the last list from the stock sheet
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    from sales work sheet, collects data from
    the last 5 entries for each sandwich as a list of lists.
    """
    sales = SHEET.worksheet("sales")
# getting columns returned as lists inserting into our columsn list
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)

#using -5 pulls the last 5 items from the list,   : colon allows for multiple spliced list values
        columns.append(column[-5:])
    return columns

# wrap main function calls in MAIN FUNCTION

def main():
    """
    main functions for the program
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

# displays text for the main functions purpose

print('Welcome to Data Automation for loveSandwiches')
#main()

sales_columns = get_last_5_entries_sales()