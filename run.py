from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials
from pyclasses import Sales

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
ACCOUNTS = GSPREAD_CLIENT.open('accounts')
PAYABLES = GSPREAD_CLIENT.open('payables')
RECEIVABLES = GSPREAD_CLIENT.open('receivables')
GENERAL_LEDGER = GSPREAD_CLIENT.open('general ledger')

def start():
    """
    Start menu where the user can choose between 4 different tasks.
    """
    print("""
                --------MENU--------
                1. Account for sale\n\
                2. Account for purchase\n\
                3. Reconcile\n\
                4. Create financial statements\n\
                    """)
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            print("Taking you to sales accounting...\n")
            print("\033c")
            sale()
            break
        if choise == '2':
            print("Taking you to purchases accounting...\n")
            purchase()
            print("\033c")
            break
        if choise == '3':
            print("Taking you account reconciliation...\n")
            reconciliation()
            print("\033c")
            break
        if choise == '4':
            print("Taking you to financial statements...\n")
            financial_statements()
            print("\033c")
            break
        print("Not a valid input please enter a number 1-4")




def sale():
    """
    Menu for accounting sales
    """
    action = Sales()
    print("""
                --------Sales--------
                1. Credit sale\n\
                2. Cash sale\n\
                3. Back to menu\n\
                    """)
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            action.credit_sale()
            print("\033c")
            break
        if choise == '2':
            cash_sale()
            print("\033c")
            break
        if choise == '3':
            start()
            print("\033c")
            break
        print("Not a valid input please enter a number 1-3")

def choose_customer():
    """
    Show existing customers and add new if not in list
    """
    existing_customers = get_worksheet_titles(RECEIVABLES)
    num = 1
    for customer in existing_customers:
        print(num, '', customer)
        num += 1
    while True:
        choise = int(input("Choose a customer: \n"))
        print("If adding a new customer, press 'n'\n")
        if choise == 'n':
            name = input('Customer name:')
            new = new_worksheet('rec', name)
            return new
        try:
            int(choise) < len(existing_customers)
        except TypeError as type_error:
            print(f"Invalid character: {type_error}, try again")
        except ValueError as value_error:
            print(f"Chosen value {value_error} is not valid, please try again")
        else:
            account_no = RECEIVABLES.worksheet(existing_customers[choise - 1]).acell('A1').value
            print(f"{existing_customers[choise - 1]} chosen. Proceeding.")
            return [existing_customers[choise - 1], account_no]

def new_worksheet(spreadsheet, name):
    """
    Add a new worksheet to spreadsheet
    Args:
        spreadsheet (name): spreadsheet to add to
    """
    print('Creating new worksheet...')
    while True:
        if spreadsheet == RECEIVABLES:
            RECEIVABLES.add_worksheet(title=name, rows=100, cols=26)
            RECEIVABLES.worksheet(name).format('A1:W1', {
                "horizontalAlignment": "RIGHT",
                "bold": True
                })
            row = first_row(RECEIVABLES, name)
            print('Worksheet created. Moving to details...')
            return row
def first_row(name, name2):
    """Adds first row to worksheet

    Args:
        name (spreadsheet): spreadsheet
        name2 (worksheet): worksheet
    """
    print('Formatting first row...')
    num = new_account_number(name)
    if name == RECEIVABLES:
        append_data(RECEIVABLES, name2, [num, 'Dr (€)', 'Cr (€)'])
        write_data(RECEIVABLES, name2)
    return num

def new_account_number(name):
    """Gets a new account number for new worksheets

    Args:
        name (var): spreadsheet to index

    Returns:
        int: new number
    """
    print('Generating account number...')
    worksheet_list = []
    for worksheet in name:
        worksheet_list.append(worksheet.title)
    A1 = name.worksheet_list[-1].acell('A1').value
    num = int(''.join(c for c in A1 if not c.isdigit()))
    num += 10
    num = f"RL{num}"
    print(f"New account number is: {num}")
    return f"RL{num}"

def write_data(name, name2):
    """Gets new data to write, then passes on to append_data

    Args:
        name (spreadsheet): spreadsheet data is added to
        name2 (worksheet): worksheet for data
    """
    print('Add new data to file:')
    print('Product:')
    while True:
        if spreadsheet == RECEIVABLES:
            choise = input('Customer name:')
            RECEIVABLES.add_worksheet(title=choise, rows=100, cols=26)
            RECEIVABLES.worksheet(choise).format('A1:W1', {
                "horizontalAlignment": "RIGHT",
                "bold": True
                })
            first_row(RECEIVABLES, choise)
            print('Worksheet created. Moving to details...')
            break
    #date = 
    
    
    append_data(name, name2, data)
    

def get_worksheet_titles(spreadsheet):
    """
    Show existing worksheet titles

    Args:
        spreadsheet (var): spreadsheet to index
    """
    print('Getting list of worksheets...')
    worksheet_list = []
    for worksheet in spreadsheet.worksheets():
        worksheet_list.append(worksheet.title)
    return worksheet_list

def purchase():
    """
    Menu for accounting purchases
    """
    print("""
                --------Purchases--------
                1. Credit purchase\n\
                2. Cash purchase\n\
                3. Back to menu\n\
                    """)
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            credit_purchase()
            print("\033c")
            break
        elif choise == '2':
            cash_purchase()
            print("\033c")
            break
        elif choise == '3':
            start()
            print("\033c")
            break
        else:
            print("Not a valid input please enter a number 1-3")
def reconciliation():
    """
    Menu for reconciling accounts
    """
    print("""
                --------Reconciliations--------
                    """)
    while True:
        choise = input("Start reconciliation?")
        if yes_or_no(choise):
            reconcile_accounts()
        if choise == 'y':
            credit_sale()
            print("\033c")
            break
        elif choise == 'n':
            print("Going back to menu...\n")
            start()
            print("\033c")
            break
        else:
            print("Not a valid input please enter a number 1-3")
def yes_or_no(question):
    """
    Function to check yes/no questions

    Args:
        question (string): question for y/n

    Returns:
        true: if input is y
        false: if input is n
    """
    while "the answer is invalid":
        reply = str(input(question+' (y/n): \n')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def list_sum(numlist):
    """converts list values to integers, then
    sums them

    Args:
        numlist (list): list of values to sum up

    Returns:
        int: sum of the values in list
    """
    new_list = [int(num) for num in numlist]
    return sum(new_list)

def append_data(sheet, worksheet, data):
    """Appends data to specified sheet

    Args:
        sheet (var): variable for the sheet to access
        worksheet(str): name of worksheet to append data
        data (list): list where each item is one column in worksheet
    """
    sheet = sheet.worksheet(worksheet)
    sheet.append_row(data)
    print(f"Successfully added data to {sheet}")

start()
