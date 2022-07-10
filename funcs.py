from random import randint
from progress.bar import ChargingBar
import gspread
from google.oauth2.service_account import Credentials
from exportpdf import sort_data

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
DATABASE = GSPREAD_CLIENT.open('database')
STOCK = GSPREAD_CLIENT.open('stock')




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

def sales_receipts_menu(customer, account):
    """
    Enters records of sales receipts into relevant accounts
    """
    print('First choose customer who made the payment\n')
    inv_nos = RECEIVABLES.worksheet(customer).col_values(3)[1:]
    print(inv_nos)
    trans_id = get_trans_id('SR')
    print(trans_id)
    invoice = None
    while True:
        invoice = input('Enter invoice number for payment:')
        try:
            amount = float(input('Enter amount received:'))
        except TypeError as typ_err:
            print(f'Value entered {typ_err} is not valid.')
            print('Please try again.')
        else:
            data = [customer, account, trans_id, amount, invoice]
            print(data)
            return data

def purchase_payments_menu(supplier, account):
    """
    Enters records of purchase payments into relevant accounts
    """
    inv_nos = PAYABLES.worksheet(supplier).col_values(2)[3:]
    print(inv_nos)
    trans_id = get_trans_id('PP')
    print(trans_id)
    invoice = None
    while True:
        invoice = input('Enter invoice number for payment:')
        if is_item_in_list(inv_nos, invoice):
            try:
                amount = float(input('Enter amount paid:'))
            except TypeError as typ_err:
                print(f'Value entered {typ_err} is not valid.')
                print('Please try again.')
            data = [supplier, account, trans_id, amount, invoice]
            print(data)
            return data
        raise ValueError(f'Invoice number {invoice} is not valid.')

def register_sales_receipt(data):
    """passes sales receipt data to append_data

    Args:
        data (list): list with data
        [customer, account number, transaction ID, amount, invoice number]
    """
    customer = data[0]
    account_no = data[1]
    trans_id = data[2]
    amount = data[3]
    inv_no = data[4]
    data_ls = [
        [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, amount]], False,
        [GENERAL_LEDGER, 'Cash', ['GL300', trans_id, amount * 0.75], True],
        [GENERAL_LEDGER, 'Sales Tax', ['GL300', trans_id, amount * 0.25], True],
        [RECEIVABLES, customer, ['Payment', -abs(amount), inv_no], False]
    ]
    append_data(data_ls)
    print(f"Outstanding balance on {customer}'s account:")
    print(RECEIVABLES.worksheet(customer).acell('H4').value())

def register_purchase_payment(data):
    """passes purchase payment data to append_data

    Args:
        data (list): list with data
        [supplier, account number, transaction ID, amount, invoice number]
    """
    supplier = data[0]
    account_no = data[1]
    trans_id = data[2]
    amount = data[3]
    inv_no = data[4]
    data_ls = [
        [GENERAL_LEDGER, 'Trade Payables', [account_no, trans_id, amount], False],
        [GENERAL_LEDGER, 'Cash', ['GL400', trans_id, amount * 0.75], True],
        [GENERAL_LEDGER, 'Sales Tax', ['GL300', trans_id, amount * 0.25], True],
        [PAYABLES, supplier, ['Payment', amount, inv_no], False]
    ]
    append_data(data_ls)
    print(f"Outstanding balance on {supplier}'s account:")
    print(PAYABLES.worksheet(supplier).acell('H4').value())

def purchases_menu():
    """creates list of items purchased
    Returns:
        list: list with items
        [[product, price]]
    """
    print(
        """
        ---Type of product(s)---
        1. Current asset
        (replenishing stock)
        2. Non-current asset
        (equipment, other materials that will last for over a year)
        """
        )
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            return how_many_items(), 'Current Assets'
        if choise == '2':
            return no_of_products(), 'Non-Current Assets'
        print('Entered value is not valid.')
        print('Please try again.')




def choose_customer():
    """Show existing customers and add new if not in list

    Returns:
        list: [account number, [address]]
    """
    existing_customers = get_worksheet_titles(RECEIVABLES)
    last_account_no = RECEIVABLES.worksheet(existing_customers[- 1]).acell('A1').value
    num = 1
    for customer in existing_customers:
        if customer != 'Base':
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
            customer = existing_customers[choise]
            account_no = RECEIVABLES.worksheet(customer).acell('A1').value
            address_row = DATABASE.worksheet('addresses').find(customer).row
            address = DATABASE.worksheet('addresses').row_values(address_row)
            print(address)
            print(f"{customer} chosen. Proceeding.")
            return [account_no, address]



def choose_supplier():
    """Show existing suppliers and add new if not in list

    Returns:
        list: [Supplier name, account no]
    """
    existing_suppliers = get_worksheet_titles(PAYABLES)
    last_account_no = PAYABLES.worksheet(existing_suppliers[- 1]).acell('A1').value
    num = 1
    for supplier in existing_suppliers:
        print(num, '', supplier)
        num += 1
    while True:
        choise = int(input("Choose a supplier: \n"))
        print("If adding a new supplier, press 'n'\n")
        if choise == 'n':
            name = input('Supplier name:')
            new = new_account_number(last_account_no)
            new_worksheet(PAYABLES, name, new)
            return [name, new]
        try:
            int(choise) < len(existing_suppliers)
        except TypeError as type_error:
            print(f"Invalid character: {type_error}, try again")
        except ValueError as value_error:
            print(f"Chosen value {value_error} is not valid, please try again")
        else:
            supplier = existing_suppliers[choise - 1]
            account_no = PAYABLES.worksheet(supplier).acell('A1').value
            print(f"{supplier} chosen. Proceeding.")
            return [supplier, account_no]




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

def how_many_items():
    """checks how many different items were ordered

    Returns:
        list: list of items ordered
    """
    items = []
    print('How many items will be added to the invoice?')
    while True:
        choise = input('Type any number of products:')
        int_choise = int(choise)
        while int_choise > 0:
            items.append(product_menu())
            int_choise -= 1
        print(items)
        return items


def no_of_products():
    """user enters no of products purchased,
    generates list with products

    Args:
        num (int): type of asset bought
    Returns:
        list: [[product, price]]
    """
    items = []
    print('Did you buy several products?')
    while True:
        choise = how_many(input('Type the amount of different products you bought:'))
        int_choise = int(choise)
        while int_choise > 0:
            items.append(enter_products())
            int_choise -= 1
        print(items)
        return items

def enter_products():
    """gets product info for non-current asset purchases

    Args:
        num1 (int): the position of product
        num2 (int): number of products to enter in total

    Returns:
        _type_: _description_
    """
    print('What product did you buy?')
    while True:
        product = input('Enter product description:')
        price = input('Enter the net value of the product:')
        return [product, float(price)]

def how_many(var):
    """prompts for an amount of something

    Args:
        var (function): input with appropriate text

    Returns:
        str: 'chosen amount'
    """
    while True:
        try:
            int(var)
        except TypeError as typ_err:
            print(f"Chosen value {typ_err} is not an integer.")
            print('Please try again.')
        else:
            return int(var)

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
    index_of = DATABASE.worksheet('transactionids')
    old_trans_ids = index_of.col_values(1)
    while True:
        trans_id = f"{ttype}{str(gen_rand_list(7))}"
        if not is_item_in_list(old_trans_ids, trans_id):
            index_of.append_row([trans_id])
        print(trans_id)
        return trans_id

def get_inv_id():
    """
    Generates a new invoice ID until the ID is unique (checks it against index of IDs)
    Appends it to index of IDs

    Args:
        ttype (str): beginning of id
        identifies transaction type

    Returns:
        str: new transaction id
    """
    index_of = DATABASE.worksheet('invoiceids')
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
        if str(item) == str(i):
            return True
    return False

def make_item_list(date: str, items: list, ttype: int, extratype:int= None):
    """generates a list of products to add to list which is appended to spreadsheets

    Args:
        date (str): date
        items (list): [product, amount]
        ttype (list): transaction type (sale = 1, purchase = 2)

    Returns:
       list: list with complete data
    """
    stock_itms = []
    grosses = []
    for itm in items:
        product = itm[0]
        amount = itm[1]
        gross = float(get_gross_total(product, amount))
        grosses.append(gross)
        if ttype == 1:
            stock_itms.append([STOCK, product, [date, '', amount, gross, gross/amount], True])
        if ttype == 2:
            stock_itms.append([STOCK, product, [date, amount, '', gross, gross/amount], True]) 
        if extratype == 1:
            stock_itms.append([GENERAL_LEDGER, 'Non-Current Assets',
                           ['GL400', product, gross], False])
    if extratype == 2:
        stock_itms.append([GENERAL_LEDGER, 'Current Assets',
                      ['GL400', 'Stock refill', gross], False])
    gross_total = float(sum(grosses))
    print(f"Gross total: {gross_total}")
    return [stock_itms, gross_total]




def sort_cr_sale_data(details: list, date: str, customer: list):
    """passes transaction data to append_data

    Args:
        details (list): [[product name, amount]]
        date (str): transaction date
        customer (list): [account number, [name, address, city, postcode, country]]
    """
    print('Writing transaction data...')
    name = customer[1][0]
    account_no = customer[0]
    address = customer[1][1:5]
    trans_id = get_trans_id('SC')
    inv_no = get_inv_id()
    print(f"Transaction ID: {trans_id}")
    print(f"Invoice number: {inv_no}")
    get_data = make_item_list(date, details, 1)
    print(f"GetData Complete: {get_data}")
    data = [name, account_no, get_data[1], trans_id, inv_no, date]
    order = []
    for itm in get_data[0]:
        order.append([itm[1], itm[2][2], itm[2][3]])
    print(order)
    write_cr_sale(data, get_data[0])
    sort_data(order, date, inv_no, trans_id, name, address)


#write data


def write_cr_sale(data, stock_list):
    """passes transaction data to append_data

    Args:
        details (list): [product name, amount]
        date (str): transaction date
        customer (list): [customer name, account number]
    """
    print('Writing transaction data...')
    name = data[0]
    account_no = data[1]
    gross_total = data[2]
    trans_id = data[3]
    inv_no = data[4]
    date = data[5]
    data_ls = [
    [GENERAL_LEDGER, 'Trade Receivables', [account_no, trans_id, gross_total], True],
    [RECEIVABLES, name, ['Invoice', gross_total, inv_no], True],
    [ACCOUNTS, 'sdb', [date, account_no, gross_total * 0.75, gross_total * 0.25, gross_total], True]
    ]
    for itm in stock_list:
        data_ls.append(itm)
    append_data(data_ls)
    end()

def write_dr_sale(details: list, date: str):
    """passes transaction data to append_data

    Args:
        details (list): product name, amount
        date (str): transaction date
    """
    print('Writing transaction data...')
    trans_id = get_trans_id('SD')
    get_data = make_item_list(date, details, 1)
    gross = get_data[1]
    data_ls = [
        [GENERAL_LEDGER, 'Sales', ['cash sale', trans_id, gross * 0.75], True],
        [GENERAL_LEDGER, 'Sales Tax', ['cash sale', trans_id, gross * 0.25], True],
        [GENERAL_LEDGER, 'Current Assets', ['sales', trans_id, gross], False],
        [ACCOUNTS, 'cash', [date, 'sales', trans_id, gross], True]
    ]
    for itm in get_data[0]:
        data_ls.append(itm)
    append_data(data_ls)
    end()

def write_cr_purchase(itms, data, acct):
    """passes transaction data to append_data

    Args:
        details (list): [product name, amount]
        date (str): transaction date
        supplier (list): [supplier name, account number]
    """
    print('Writing transaction data...')
    account_no = data[2]
    name = data[1]
    price = data[3:5]
    inv_no = data[5]
    date = data[0]
    if acct == 'Non-Current Assets':
        get_data = make_item_list(date, itms, 2, 1)
    else:
        get_data = make_item_list(date, itms, 2, 2)
    gross = float(get_data[1])
    data_ls = [
    [GENERAL_LEDGER, 'Trade Payables', [account_no, inv_no, gross], True],
    [PAYABLES, name, ['Invoice', gross, inv_no], True],
    [ACCOUNTS, 'pdb', [date, account_no, price[0]], True]
    ]
    for itm in get_data[0]:
        data_ls.append(itm)
    append_data(data_ls)
    end()

def write_dr_purchase(itms, data, acct):
    """passes transaction data to append_data

    Args:
        details (list): product name, amount
        date (str): transaction date
    """
    print('Writing transaction data...')
    account_no = data[2]
    name = data[1]
    price = data[3:5]
    inv_no = data[5]
    date = data[0]
    if acct == 'Non-Current Assets':
        get_data = make_item_list(date, itms, 2, 1)
    else:
        get_data = make_item_list(date, itms, 2, 2)
    gross = float(get_data[1])
    data_ls = [
    [GENERAL_LEDGER, 'Trade Payables', [account_no, inv_no, gross], True],
    [PAYABLES, name, ['Invoice', gross, inv_no], True],
    [ACCOUNTS, 'pdb', [date, account_no, price[0]], True]
    ]
    for itm in get_data[0]:
        data_ls.append(itm)
    append_data(data_ls)
    end()




#gspread stuff

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
    """Updates specified sheet with data

    Args:
        data (list): list of data
        [[spreadsheet, worksheet, data, left?]]
            spreadsheet (var): spreadsheet where worksheet is
            worksheet (str): worksheet data is added to
            data (list): list of data to write to worksheet
            left? (bool): True if data is added to left side in accounts (Dr)
                          False if added to right (Cr)
    """
    print('Reading data...')
    with ChargingBar('Writing data|', max=len(data_list)) as progress_bar:
        for data in data_list:
            spreadsheet = data[0]
            worksheet = data[1]
            data_to_write = data[2]
            sheet = spreadsheet.worksheet(worksheet)
            vals = sheet.get_all_values()[3:]
            continue_loop = True
            if data[3]:
                vals.append(data_to_write[0:3])
            else:
                for val in vals:
                    while True:
                        if not val[3] and continue_loop:
                            del val[3:]
                            val.extend(data_to_write[3:])
                            continue_loop = False
                        break
            sheet.update('A4:F', vals)
            progress_bar.next()
    print('Operation Successful.')
