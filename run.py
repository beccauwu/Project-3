from funcs import *

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
    trans_type = cash_or_credit('Sale')
    if trans_type == 1:
        customer = choose_customer()
        write_cr_sale(details, date, customer)
    elif trans_type == 2:
        write_dr_sale(details, date)



def purchase():
    """
    Menu for accounting purchases
    """
    details = purchases_menu()
    date = get_date()
    trans_type = cash_or_credit('Sale')
    if trans_type == 1:
        customer = choose_customer()
        write_cr_purchase(details, date, customer)
    elif trans_type == 2:
        write_dr_purchase(details, date)

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
