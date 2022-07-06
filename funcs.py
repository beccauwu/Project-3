from pprint import pprint
from random import randint
from progress.bar import ChargingBar
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
INDEX = GSPREAD_CLIENT.open('index')
STOCK = GSPREAD_CLIENT.open('stock')

def choose_customer():
    """Show existing customers and add new if not in list

    Returns:
        list: [Customer name, account no]
    """
    existing_customers = get_worksheet_titles(RECEIVABLES)
    last_account_no = RECEIVABLES.worksheet(existing_customers[- 1]).acell('A1').value
    num = 1
    for customer in existing_customers:
        print(num, '', customer)
        num += 1
    while True:
        choise = int(input("Choose a customer: \n"))
        print("If adding a new customer, press 'n'\n")
        if choise == 'n':
            name = input('Customer name:')
            new = new_account_number(last_account_no)
            new_worksheet(RECEIVABLES, name, new)
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

def new_worksheet(spreadsheet, title, code):
    """creates a new worksheet using a base template

    Args:
        spreadheet (const): spreadsheet to add to
        title (str): new worksheet title
        code (str): value of A1
    """
    new_sheet = spreadsheet.duplicate_sheet('Base')
    new_sheet.update_title(title)
    new_sheet.update('A1', code)

def new_account_number(last):
    """Gets a new account number for new worksheets

    Args:
        ssh (var): spreadsheet to index

    Returns:
        int: new number
    """
    code = last[0:2]
    num = int(''.join(c for c in last if c.isdigit()))
    num += 10
    print(f"New account number is: RL{num}")
    return f"{code}{num}"

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

def append_data(data_list):
    """Appends data to specified sheet

    Args:
        data (list): list of data
        [spreadsheet, worksheet, data]
    """
    print('Reading data...')
    with ChargingBar('Writing data|', max=len(data_list)) as progress_bar:
        for data in data_list:
            spreadsheet = data[0]
            worksheet = data[1]
            data_to_write = data[2]
            sheet = spreadsheet.worksheet(worksheet)
            sheet.append_row(data_to_write)
            progress_bar.next()
    print('Operation Successful.')

def gen_rand_list(num):
    """generates a list with random digits

    Args:
        num (int): length of list

    Returns:
        str: string with random digits
    """
    rand_str = ""
    while len(rand_str) <= num:
        rand_str += str(randint(0, 9))
    return rand_str

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
            print("\033c")
            return ['Soap Bar', products]
        if choise == '2':
            products = how_many(input("How many bottles"))
            print(f"Got it. {products} bottles of soap")
            print("\033c")
            return ['Liquid Soap', products]
        if choise == '3':
            products = how_many(input("How many jars?\n"))
            print(f"Got it. {products} jars of coconut oil")
            print("\033c")
            return ['Coconut Oil', products]
        if choise == '4':
            products = how_many(input("How many cans?\n"))
            print(f"Got it. {products} cans of lute")
            print("\033c")
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
    print(f"--------{trans_type}s--------\n1. Credit {trans_type}\n2. Cash {trans_type}\n")
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
        date = input('Enter transaction date: (DDMMYYYY)')
        str(date)
        if check_if_date(date):
            return f"{date[0:2]}.{date[2:4]}.{date[4:8]}"

def check_if_date(date):
    """Checks if date is the correct format
    and validates date

    Args:
        date (str): date to check

    Returns:
        True if is correct format,
        False if not
    """
    #correct length?
    if len(date) == 8:
        #if uneven month, see if value of days is less than 32
        if int(date[1]) % 2 != 0:
            try:
                int(date[0:2]) < 32
            except ValueError as uneven:
                print(f'The month entered does not have {uneven} days.')
                print('Please try again.')
                return False
        #if even month see if value of days is less than 31
        elif int(date[1]) % 2 == 0:
            try:
                int(date[0:2]) < 31
            except ValueError as even:
                print(f'The month entered does not have {even} days.')
                print('Please try again.')
                return False
        #if february leap year see if value of days less than 30
        elif int(date[4:8]) % 4 == 0 and int(date[4:8]) % 100 != 0:
            try:
                int(date[0:2]) < 30
            except ValueError as leap:
                print(f'The month entered does not have {leap} days.')
                print('Please try again.')
                return False
        #if february non leap year see if value of days less than 29
        elif int(date[4:8]) % 4 != 0:
            try:
                int(date[0:2]) < 29
            except ValueError as non_leap:
                print(f'The month entered does not have {non_leap} days.')
                print('Please try again.')
                return False
        #check that month number is less than 13
        try:
            int(date[2:4]) < 13
        except ValueError as val_err:
            print(f"There isn't a month number {val_err}.")
            print('Please try again.')
            return False
        else:
            return True
    print(f"The date entered ({date}) is not of correct format (DDMMYYYY),")
    print(f"you have entered {len(date)} characters instead of 8.")
    print('Please try again.')
    return False

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

def get_trans_id(ttype: str):
    """Generates a new transaction ID
    and appends it to index of IDs

    Args:
        ttype (str): beginning of id
        identifies transaction type

    Returns:
        str: new transaction id
    """
    index_of = INDEX.worksheet('transactions')
    old_trans_ids = index_of.col_values(1)
    while True:
        trans_id = f"{ttype}{str(gen_rand_list(3))}"
        if not is_item_in_list(old_trans_ids, trans_id):
            index_of.append_row([trans_id])
            return trans_id

def get_inv_id():
    """Generates a new invoice ID
    and appends it to index of IDs

    Args:
        ttype (str): beginning of id
        identifies transaction type

    Returns:
        str: new transaction id
    """
    index_of = INDEX.worksheet('invoices')
    old_inv_ids = index_of.col_values(1)
    while True:
        inv_id = f"INV{str(gen_rand_list(3))}"
        if not is_item_in_list(old_inv_ids, inv_id):
            index_of.append_row([inv_id])
            return inv_id

def is_item_in_list(lst, item):
    """Checks an item against an index of list

    Args:
        lst (list): list to index
        item (any): item to check

    Returns:
        boolean: True if it exists,
        False if not
    """
    for i in lst:
        if str(item) != str(i):
            return False
    return True

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
    trans_id = get_trans_id('SC')
    inv_no = f"INV{str(gen_rand_list(2))}"
    data_ls = [
    [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, gross]],
    [GENERAL_LEDGER, 'Current Assets', ['', '', '', 'GL300', trans_id, gross]],
    [RECEIVABLES, name, ['Invoice', gross, inv_no]],
    [ACCOUNTS, 'sdb', [date, account_no, gross * 0.75, gross * 0.25, gross]],
    [STOCK, product, [date, '', amount, gross, gross/amount]]
    ]
    append_data(data_ls)

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
    data_ls = [
        [GENERAL_LEDGER, 'Sales', ['cash sale', trans_id, gross * 0.75]],
        [GENERAL_LEDGER, 'Sales Tax', ['cash sale', trans_id, gross * 0.25]],
        [GENERAL_LEDGER, 'Current Assets', ['', '', '', ['sales', trans_id, gross]]],
        [ACCOUNTS, 'cash', [date, 'sales', trans_id, gross]],
        [STOCK, product, [date, '', amount, gross, gross/amount]]
    ]
    append_data(data_ls)

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
    data_ls = [
    [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, gross]],
    [GENERAL_LEDGER, 'Current Assets', ['', '', '', 'GL300', trans_id, gross]],
    [RECEIVABLES, name, ['Invoice', gross, inv_no]],
    [ACCOUNTS, 'sdb', [date, account_no, gross * 0.75, gross * 0.25, gross]],
    [STOCK, product, [date, '', amount, gross, gross/amount]]
    ]
    append_data(data_ls)

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
    data_ls = [
        [GENERAL_LEDGER, 'Sales', ['cash sale', trans_id, gross * 0.75]],
        [GENERAL_LEDGER, 'Sales Tax', ['cash sale', trans_id, gross * 0.25]],
        [GENERAL_LEDGER, 'Current Assets', ['', '', '', ['sales', trans_id, gross]]],
        [ACCOUNTS, 'cash', [date, 'sales', trans_id, gross]],
        [STOCK, product, [date, '', amount, gross, gross/amount]]
    ]
    append_data(data_ls)