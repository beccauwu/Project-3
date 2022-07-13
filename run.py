import time
import funcs

def start():
    """
    Start menu where the user can choose between 4 different tasks.
    """
    print("""
                --------MENU--------
                1. Account for sales\n\
                2. Account for purchases\n\
                3. Account for sales receipts\n\
                4. Account for purchase payments\n\
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
            print("Taking you sales receipts...\n")
            sales_receipt()
            print("\033c")
            break
        if choise == '4':
            print("Taking you to purchase payments...\n")
            purchase_payments()
            print("\033c")
            break
        print("Not a valid input please enter a number 1-4")



def sale():
    """
    Menu for accounting sales
    """
    details = funcs.how_many_items()
    date = funcs.get_date()
    trans_type = funcs.cash_or_credit('Sale')
    if trans_type == 1:
        customer = funcs.choose_customer()
        funcs.sort_cr_sale_data(details, date, customer)

    elif trans_type == 2:
        funcs.write_dr_sale(details, date)



def purchase():
    """
    Menu for accounting purchases
    """
    details = funcs.purchases_menu()
    products = details[0]
    date = funcs.get_date()
    trans_type = funcs.cash_or_credit('Purchase')
    net_price = input('Enter the net price of purchase:')
    gross_price = input('Enter the gross price of purchase:')
    if trans_type == 1:
        supplier = funcs.choose_supplier()
        invoice_num = input('Enter the invoice number:')
        data = [date, supplier[0], supplier[1], net_price, gross_price, invoice_num]
        funcs.write_cr_purchase(products, data, details[1])
    elif trans_type == 2:
        funcs.write_dr_purchase(products, date, details[1])

def sales_receipt():
    """
    registers sales receipts
    """
    customer = funcs.choose_customer()
    data = funcs.sales_receipts_menu(customer[1][0], customer[0])
    funcs.register_sales_receipt(data)

def purchase_payments():
    """
    registers purchase payments
    """
    supplier = funcs.choose_supplier()
    data = funcs.purchase_payments_menu(supplier[0], supplier[1])
    funcs.register_purchase_payment(data)

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

def first():
    """
    Prints out project logo as text and waits for 2 seconds
    """
    lines = [
        '               :        .',
        '               :       / \  /\  .',
        '               :      /   \/  \/ \  .——>',
        '               :     /          __\/',
        '               :    /      __  |  |',
        '               :   /  __  |  | |  |',
        '               :  /  |  | |  | |  |',
        '               : /   |  | |  | |  |',
        '               :/    |  | |  | |  |',
        '               *************************\n'
    ]
    for line in lines:
        print(line)
        time.sleep(0.1)
    start()

first()
