from pprint import pprint
from random import randint
import gspread
from google.oauth2.service_account import Credentials

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
STOCK = GSPREAD_CLIENT.open('stock')

def choose_customer():
    """Show existing customers and add new if not in list

    Returns:
        list: [Customer name, account no]
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
            return [name, new]
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
            RECEIVABLES.add_worksheet(title=name, rows=100, cols=26)
            RECEIVABLES.worksheet(choise).format('A1:W1', {
                "horizontalAlignment": "RIGHT",
                "bold": True
                })
            first_row(RECEIVABLES, choise)
            print('Worksheet created. Moving to details...')
            break
    #date = 
    

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

def gen_rand_list(num):
    """generates a list with random digits

    Args:
        num (int): length of list

    Returns:
        str: string with random digits
    """
    rand_list = []
    while len(rand_list) <= num:
        rand_list.append(randint(0, 9))
    return str(rand_list)

def product_menu():
    """
    prints products and based on choise calls a parent
    """
    print(
        """
        ---Products---
        1. Soap Bar
        2. Liquid Soap
        3. Coconut Oil
        4. NaOH
        """
        )
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            products = how_many(input("How many soap bars?\n"))
            print(f"Got it. {products} bars of soap")
            return [1, products]
        if choise == '2':
            products = how_many(input("How many bottles"))
            print(f"Got it. {products} bottles of soap")
            return [2, products]
        if choise == '3':
            products = how_many(input("How many jars?\n"))
            print(f"Got it. {products} jars of coconut oil")
            return [3, products]
        if choise == '4':
            products = how_many(input("How many cans?\n"))
            print(f"Got it. {products} cans of lute")
            return [4, products]
        print("Not a valid input please enter a number 1-4")

def how_many(var):
    """prompts for an amount of something

    Args:
        var (function): input with appropriate text

    Returns:
        str: 'chosen amount'
    """
    while True:
        products = var
        try:
            int(products)
        except TypeError as typ_err:
            print(f"Chosen value {typ_err} is not an integer.")
            print('Please try again.')
        else:
            return products

def cash_or_credit():
    """
    chacks type of transaction
    """
    print("""
                --------Sales--------
                1. Credit sale\n\
                2. Cash sale\n\
                    """)
    while True:
        choise = input("Choose type of sale: \n")
        if choise == '1':
            print('Chose credit sale \n')
            return 1
        if choise == '2':
            print('Chose cash sale')
            return 2
        print("Not a valid input please enter a number 1-3")

def get_date():
    """Gets transaction date from user input
    and checks if it is valid

    Returns:
        str: the date
    """
    while True:
        date = input('Enter transaction date: (DDMM)')
        date_list = []
        str(date)
        if check_if_date(date):
            date_list.append(str(date[0:1]))
            date_list.append(str(date[2:3]))
            return date_list

def check_if_date(date):
    """Checks if date is the correct format

    Args:
        date (str): date to check

    Returns:
        boolean: True if is correct format,
        False if not
    """
    if len(date) == 4:
        return True
    print(len(date))
    print('The entered date is invalid')
    print('Please try again')
    return False

def sales_trans_id(var):
    """generates a transaction ID

    Args:
        var (int): transaction type

    Returns:
        str: completed transaction ID
    """
    trans_id = 'S'
    if var == 1:
        trans_id += 'C'
    elif var == 2:
        trans_id += 'D'
    trans_id += gen_rand_list(3)
    return trans_id

def write_transaction(product, amount, date, trans_type, customer, inv_no, gross, trans_id):
    """
    Writes transaction to accounts
    """
    sales_credit_append_list = [
    [GENERAL_LEDGER, 'Trade Receivables', [customer, trans_id, gross]],
    [GENERAL_LEDGER, 'Current Assets', ['', '', '', customer, trans_id, gross]],
    [RECEIVABLES, customer, ['Invoice', gross, inv_no]],
    [ACCOUNTS, 'sdb', [f"{date[1]}.{date[2]}", customer, net, tax, gross]],
    [STOCK, product, [f"{date[1]}.{date[2]}", '', amount, gross, gross/amount]]
    ]
    net = int(gross) * 0.75
    tax = int(gross) * 0.25
    if trans_type == 1:
        append_data(
            GENERAL_LEDGER, 'Trade Receivables', [customer, trans_id, gross]
            )
        append_data(
            GENERAL_LEDGER, 'Current Assets', ['', '', '', customer, trans_id, gross]
            )
        append_data(
            RECEIVABLES, customer, ['Invoice', gross, inv_no]
            )
        append_data(
            ACCOUNTS, 'sdb', [f"{date[1]}.{date[2]}", customer, net, tax, gross]
            )
        append_data(
            STOCK, product, [f"{date[1]}.{date[2]}", '', amount, gross, gross/amount]
        )
    if trans_type == 2:
        append_data(
            GENERAL_LEDGER, 'Sales', [customer, trans_id, gross * 0.75]
        )
        append_data(
            GENERAL_LEDGER, 'Sales Tax', [customer, trans_id, gross * 0.25]
        )
        append_data(
            GENERAL_LEDGER,
            'Current Assets', ['', '', '', [customer, trans_id, gross]]
        )
        append_data(
            ACCOUNTS, 'cash', [date, customer[1], customer[0], gross]
        )
        append_data(
            STOCK, product, [f"{date[1]}.{date[2]}", '', amount, gross, gross/amount]
        )
