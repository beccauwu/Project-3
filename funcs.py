from pprint import pprint
from random import randint
from progress.bar import FillingCirclesBar
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
            new = new_worksheet(RECEIVABLES, name)
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

def choose_supplier():
    """Show existing suppliers and add new if not in list

    Returns:
        list: [Supplier name, account no]
    """
    existing_suppliers = get_worksheet_titles(PAYABLES)
    num = 1
    for supplier in existing_suppliers:
        print(num, '', supplier)
        num += 1
    while True:
        choise = int(input("Choose a supplier: \n"))
        print("If adding a new supplier, press 'n'\n")
        if choise == 'n':
            name = input('Supplier name:')
            new = new_worksheet(PAYABLES, name)
            return [name, new]
        try:
            int(choise) < len(existing_suppliers)
        except TypeError as type_error:
            print(f"Invalid character: {type_error}, try again")
        except ValueError as value_error:
            print(f"Chosen value {value_error} is not valid, please try again")
        else:
            account_no = RECEIVABLES.worksheet(existing_suppliers[choise - 1]).acell('A1').value
            print(f"{existing_suppliers[choise - 1]} chosen. Proceeding.")
            return [existing_suppliers[choise - 1], account_no]

def new_worksheet(spreadsheet, title):
    """creates a new worksheet using a base template

    Args:
        spreadheet (const): spreadsheet to add to
        title (str): new worksheet title
    """
    new_sheet = spreadsheet.duplicate_sheet('Base')
    new_sheet.update_title(title)
    new_sheet.update('A1')

def new_rl_account_number(ssh):
    """Gets a new account number for new worksheets

    Args:
        ssh (var): spreadsheet to index

    Returns:
        int: new number
    """
    print('Generating account number...')
    wsh_list = [wsh.title for wsh in ssh]
    A1 = get_cell_val(RECEIVABLES, wsh_list[-1], 'A1')
    num = int(''.join(c for c in A1 if c.isdigit()))
    num += 10
    print(f"New account number is: RL{num}")
    return f"RL{num}"

def get_cell_val(ssh, wsh, cell):
    """Gets cell value from worksheet

    Args:
        ssh (const): spreadsheet to access
        wsh (str): worksheet in spreadsheet
        cell (str): cell to read value from

    Returns:
        str: cell calue
    """
    cv = ssh.worksheet(wsh).acell(cell).value
    return cv

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

def append_data(data):
    """Appends data to specified sheet

    Args:
        data (list): list of data
        [spreadsheet, worksheet, data]
    """
    print('Adding data...')
    list_of_things = data
    spreadsheet = list_of_things[0]
    worksheet = list_of_things[1]
    data_to_write = list_of_things[2]
    sheet = spreadsheet.worksheet(worksheet)
    sheet.append_row(data_to_write)
    print(f"Successfully added data to {worksheet}")

def gen_rand_list(num):
    """generates a list with random digits

    Args:
        num (int): length of list

    Returns:
        str: string with random digits
    """
    rand_str = []
    while len(rand_str) <= num:
        rand_str += randint(0, 9)
    return str(rand_str)

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
            return ['Soap Bar', products]
        if choise == '2':
            products = how_many(input("How many bottles"))
            print(f"Got it. {products} bottles of soap")
            return ['Liquid Soap', products]
        if choise == '3':
            products = how_many(input("How many jars?\n"))
            print(f"Got it. {products} jars of coconut oil")
            return ['Coconut Oil', products]
        if choise == '4':
            products = how_many(input("How many cans?\n"))
            print(f"Got it. {products} cans of lute")
            return ['NaOH', products]
        print("Not a valid input please enter a number 1-4")

def purchases_menu():
    """
    prints products and based on choise calls a parent
    """
    print(
        """
        ---Type of product(s)---
        1. Current asset 
        (replenishing stock, every day business expenses, 
        new items for sale)
        2. Non-current asset
        (equipment, other materials that will last for over a year)
        """
        )
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            products = how_many(input("How many soap bars?\n"))
            print(f"Got it. {products} bars of soap")
            return ['Soap Bar', products]
        if choise == '2':
            products = how_many(input("How many bottles"))
            print(f"Got it. {products} bottles of soap")
            return ['Liquid Soap', products]
        if choise == '3':
            products = how_many(input("How many jars?\n"))
            print(f"Got it. {products} jars of coconut oil")
            return ['Coconut Oil', products]
        if choise == '4':
            products = how_many(input("How many cans?\n"))
            print(f"Got it. {products} cans of lute")
            return ['NaOH', products]
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
            return int(products)

def cash_or_credit(trans_type: str):
    """
    checks type of transaction
    """
    print(f"--------{trans_type}s--------\n1. Credit {trans_type}\n\2. Cash {trans_type}\n")
    while True:
        choise = input(f"Choose type of {trans_type.lower()}: \n")
        if choise == '1':
            print(f'Chose credit {trans_type.lower()} \n')
            return 1
        if choise == '2':
            print(f'Chose cash {trans_type.lower()}')
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
        str(date)
        if check_if_date(date):
            return f"{date[0:2]}.{date[2:4]}."

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

def get_gross_total(product: str, amount: int):
    """calculates the gross total of a transaction

    Args:
        product (str): product sold
        amount (int): amount sold

    Returns:
        _type_: _description_
    """
    print('Calculating the gross total of your sale...')
    product_prices = {
        'Soap Bar': 6,
        'Liquid Soap': 5,
        'Coconut Oil': 8,
        'NaOH': 20,
    }
    return int(product_prices.get(product) * amount)

def write_cr_sale(details: list, date: str, customer: list):
    """passes transaction data to append_data

    Args:
        details (list): [product name, amount]
        date (str): transaction date
        customer (list): [customer name, account number]
    """
    print('Writing transaction data...')
    product = details[0]
    amount = details[1]
    gross = get_gross_total(product, amount)
    account_no = customer[1]
    name = customer[0]
    trans_id = f"SC{gen_rand_list(3)}"
    inv_no = f"INV{gen_rand_list(2)}"
    sales_append_ls = [
    [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, gross]],
    [GENERAL_LEDGER, 'Current Assets', ['', '', '', 'GL300', trans_id, gross]],
    [RECEIVABLES, name, ['Invoice', gross, inv_no]],
    [ACCOUNTS, 'sdb', [f"{date[0]}.{date[1]}", account_no, gross * 0.75, gross * 0.25, gross]],
    [STOCK, product, [f"{date[0]}.{date[1]}", '', amount, gross, gross/amount]]
    ]
    for data in sales_append_ls:
        data_index = sales_append_ls.index(data) + 1
        list_length = len(sales_append_ls)
        print(f"Writing data ({data_index}/{list_length}")
        append_data(data)

def write_dr_sale(details: list, date: str):
    """passes transaction data to append_data

    Args:
        details (list): product name, amount
        date (str): transaction date
    """
    print('Writing transaction data...')
    product = details[0]
    amount = details[1]
    gross = get_gross_total(product, amount)
    trans_id = f"SD{gen_rand_list(3)}"
    sales_append_ls = [
        [GENERAL_LEDGER, 'Sales', ['cash sale', trans_id, gross * 0.75]],
        [GENERAL_LEDGER, 'Sales Tax', ['cash sale', trans_id, gross * 0.25]],
        [GENERAL_LEDGER, 'Current Assets', ['', '', '', ['sales', trans_id, gross]]],
        [ACCOUNTS, 'cash', [f"{date[0]}.{date[1]}", 'sales', trans_id, gross]],
        [STOCK, product, [f"{date[0]}.{date[1]}", '', amount, gross, gross/amount]]
    ]
    bar = FillingCirclesBar('Writing data', max=5)
    for data in sales_append_ls:
        # data_index = sales_append_ls.index(data) + 1
        # list_length = len(sales_append_ls) + 1
        # print(f"Writing data ({data_index}/{list_length}")
        append_data(data)
        bar.next()

def write_cr_purchase(details: list, date: str, customer: list):
    """passes transaction data to append_data

    Args:
        details (list): [product name, amount]
        date (str): transaction date
        customer (list): [customer name, account number]
    """
    print('Writing transaction data...')
    product = details[0]
    amount = details[1]
    gross = get_gross_total(product, amount)
    account_no = customer[1]
    name = customer[0]
    trans_id = f"SC{gen_rand_list(3)}"
    inv_no = f"INV{gen_rand_list(2)}"
    sales_append_ls = [
    [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, gross]],
    [GENERAL_LEDGER, 'Current Assets', ['', '', '', 'GL300', trans_id, gross]],
    [RECEIVABLES, name, ['Invoice', gross, inv_no]],
    [ACCOUNTS, 'sdb', [f"{date[0]}.{date[1]}", account_no, gross * 0.75, gross * 0.25, gross]],
    [STOCK, product, [f"{date[0]}.{date[1]}", '', amount, gross, gross/amount]]
    ]
    for data in sales_append_ls:
        data_index = sales_append_ls.index(data) + 1
        list_length = len(sales_append_ls) + 1
        print(f"Writing data ({data_index}/{list_length}")
        append_data(data)

def write_dr_purchase(details: list, date: str):
    """passes transaction data to append_data

    Args:
        details (list): product name, amount
        date (str): transaction date
    """
    print('Writing transaction data...')
    product = details[0]
    amount = details[1]
    gross = get_gross_total(product, amount)
    trans_id = f"SD{gen_rand_list(3)}"
    sales_append_ls = [
        [GENERAL_LEDGER, 'Sales', ['cash sale', trans_id, gross * 0.75]],
        [GENERAL_LEDGER, 'Sales Tax', ['cash sale', trans_id, gross * 0.25]],
        [GENERAL_LEDGER, 'Current Assets', ['', '', '', ['sales', trans_id, gross]]],
        [ACCOUNTS, 'cash', [f"{date[0]}.{date[1]}", 'sales', trans_id, gross]],
        [STOCK, product, [f"{date[0]}.{date[1]}", '', amount, gross, gross/amount]]
    ]
    for data in sales_append_ls:
        data_index = sales_append_ls.index(data) + 1
        list_length = len(sales_append_ls) + 1
        print(f"Writing data ({data_index}/{list_length}")
        append_data(data)