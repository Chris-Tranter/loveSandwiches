import gspread
from google.oauth2.service_account import Credentials

# All constant variables in python have capital letters!
# SET the scope and list the API's available

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Pulling from the imported gspread were retrieving the service account and passing it our JSON

CREDS = Credentials.from_service_account_file('creds.JSON')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('loveSandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)