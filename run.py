import gspread
from google.oauth2.service_account import Credentials
from funcs import product_menu, get_date, cash_or_credit, choose_customer, write_cr_transaction, write_dr_transaction

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
    details = product_menu()
    date = get_date()
    trans_type = cash_or_credit()
    if trans_type == 1:
        customer = choose_customer()
        write_cr_transaction(details, date, customer)
    elif trans_type == 2:
        write_dr_transaction(details, date)



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


start()
