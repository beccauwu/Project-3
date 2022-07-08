import webbrowser
from collections import namedtuple
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

Creator = namedtuple("Creator", ["name", "email", "phone_num", "account", "vat_reg_no"])
Customer = namedtuple("Customer", ["name", "address", "city", "postcode", "country"])
File = namedtuple("File", ["filename", "font_size", "line_height"])
InvData = namedtuple("InvData", ["amount", "itm", "gross_total",
                                 "net_per_one", "net_total", "vat"])
PdfInvoice = namedtuple("PdfInvoice", ["date", "due", "invoice_num",
                                       'reference_num', "creator", "customer", "file"])
Row1 = namedtuple('Row1', ['col1', 'col2', 'col3', 'col4'])
Row2 = namedtuple('Row2', ['col1', 'col2', 'col3', 'col4', 'col5', 'col6'])
Row3 = namedtuple('Row2', ['col1'])

title_style = ParagraphStyle('title',
                                fontName='Helvetica-Bold',
                                fontSize=12,
                                alignment=TA_RIGHT)
small_style = ParagraphStyle('title',
                            fontName='Helvetica',
                            fontSize=8,
                            alignment=TA_RIGHT)
bold_style = ParagraphStyle('bold',
                            fontName='Helvetica-Bold',
                            fontSize=10,
                            alignment=TA_RIGHT)
normal_style = ParagraphStyle('normal',
                            fontName='Helvetica',
                            fontSize=10,
                            alignment=TA_LEFT)
price_bold = ParagraphStyle('bold',
                            fontName='Helvetica-Bold',
                            fontSize=10,
                            alignment=TA_CENTER)
price_normal = ParagraphStyle('normal',
                            fontName='Helvetica',
                            fontSize=10,
                            alignment=TA_CENTER)
footer_first = ParagraphStyle('footerbold',
                                fontName="Helvetica-Bold",
                                fontSize=8,
                                alignment=TA_CENTER)
footer_second = ParagraphStyle('footer',
                                fontName="Helvetica",
                                fontSize=8,
                                alignment=TA_CENTER)

def generate_pdf(invoice_num, filename, vat_no, tbl_one, tbl_two, summary, sammount):
    """Generates an invoice as pdf from data provided
    Args:
        date (str): invoice date
        filename (str): invoice filename
        vat_no (str): business VAT registration number
        tbl_one (list): table containing the first information on document
        tbl_two (list): table containing purchase information
    """
    pdf_content = []
    headers = [
        Paragraph("INVOICE", title_style),
        Spacer(1, 2),
        invoice_num,
        Spacer(1, 20)
    ]
    main_contents = [
        tbl_one,
        Spacer(1, 20),
        tbl_two,
        Spacer(1, 20),
        summary[0][0],
        summary[0][1],
        summary[1][0],
        summary[1][1],
        summary[2][0],
        summary[2][1],
        Spacer(1, sammount)
    ]
    footers = [
        Paragraph("E&OE", footer_first),
        Paragraph("Business is registered for VAT:", footer_first),
        Paragraph(vat_no, footer_second)
    ]
    for header in headers:
        pdf_content.append(header)
    for main in main_contents:
        pdf_content.append(main)
    for footer in footers:
        pdf_content.append(footer)
    SimpleDocTemplate(filename, pagesize=A4,
                        rightMargin=12, leftMargin=12,
                        topMargin=12, bottomMargin=6).build(pdf_content)

def sort_data(orders:list, date, inv_num, ref_num, name, address: list):
    """
    creates list with ordered items and their attributes, passes
    them then onto create_content
    """
    items = []
    creator = Creator('Test User', 'test@gmail.com', '098912312','DE1921 3210 9381 8211', 'SE00000000001')
    customer = Customer(name, address[0], address[1], address[2], address[3])
    print(f"customer: {customer}")
    file = File("Invoice.pdf", 12, 5)
    print("""
          ---Customer Type---
          1. Private
          2. Business
          """)
    while True:
        choise = input('Choose customer type:')
        if choise == '1':
            for order in orders:
                item = set_invoice_data_private(order[0], order[1], order[2])
                items.append(item)
        if choise == '2':
            for order in orders:
                item = set_invoice_data_business(order[0], order[1], order[2])
                items.append(item)
        pdf_inv = PdfInvoice(date, due_date(date), inv_num, ref_num, creator, customer, file)
        create_content(pdf_inv, items)
        break

def set_invoice_data_private(itm, amount, gross):
    """Sets invoice data for private purchases

    Args:
        itm (str): item ordered
        amount (int): amount of items ordered
        gross (float): gross price for one item

    Returns:
        var: invoice data as a namedtuple
    """
    gr_tot = gross
    gr_per_one = float(gr_tot) / float(amount)
    nt_per_one = str(round(float(gr_per_one * 0.75), 2))
    nt_tot = str(round(float(gr_tot * 0.75), 2))
    tx_tot = str(round(float(gr_tot * 0.25), 2))
    inv_data = InvData(amount, itm, gr_tot, nt_per_one, nt_tot, tx_tot)
    return inv_data

def set_invoice_data_business(amount, itm, gross):
    """sets invoice data for business purchases -
    checks if business is excempt from vat and adjusts amounts
    accordingly

    Args:
        amount (int): amount of items ordered
        itm (str): item ordered
        gross (float): total price for item

    Returns:
        var: order info inside a namedtuple
    """
    gr_tot = float(gross)*float(amount)
    nt_per_one = str(round(float(gross * 0.75), 2))
    nt_tot = str(round(float(gr_tot * 0.75), 2))
    tx_tot = str(round(float(gr_tot * 0.25), 2))
    if vat_excempt():
        inv_data = InvData(amount, itm, nt_tot, nt_per_one, nt_tot, 0)
    else:
        inv_data = InvData(amount, itm, gr_tot, nt_per_one, nt_tot, tx_tot)
    return inv_data

def due_date(date):
    """returns due date by shitfing month by one

    Args:
        date (str): invoise issue date

    Returns:
        str: invoice due date
    """
    if int(date[3]) == 0 and int(date[4]) != 9:
        return f"{date[0:2]}.0{int(date[4]) + 1}.{date[6:10]}"
    if int(date[3]) == 0:
        return f"{date[0:2]}.10.{date[6:10]}"
    if int(date[3]) == 1 and int(date[4]) != 2:
        return f"{date[0:2]}.1{int(date[4]) + 1}.{date[6:10]}"
    if int(date[3]) == 1 and int(date[9]) != 9:
        return f"{date[0:2]}.01.{date[6:9]}{date[9]}"
    if int(date[3]) == 1:
        return f"{date[0:2]}.01.{date[6:8]}{int(date[8]) + 1}0"

def vat_excempt():
    """checks if business is vat excempt

    Returns:
        boolean: true if is, false if not
    """
    while True:
        choise = input("Is the customer VAT excempt? (y/n)")
        if choise in ('y', 'Y'):
            print('Customer is VAT excempt.')
            return True
        if choise in ('n', 'N'):
            print('Customer is not VAT excempt.')
            return False
        print('Invalid choise, please try again')

def create_content(pdf_invoice_obj, itms:list):
    """creates tables for invoice based on ordered items

    Args:
        pdf_invoice_obj (var): PdfInvoice namedtuple
        itms (var): InvData namedtuple for each item
    """
    inv_num = Paragraph(f"{pdf_invoice_obj.invoice_num}", small_style)
    filename = pdf_invoice_obj.file.filename
    vat_no = f"{pdf_invoice_obj.creator.vat_reg_no}"
    nets = []
    grosses = []
    taxes = []
    space = 420
    rh = [[20, 20], [20, 20, 20, 20, 20, 20, 20]]
    tbl1 = [
        Row1(Paragraph("Date:", bold_style),
             Paragraph(f"{pdf_invoice_obj.date}", normal_style), "",
             Paragraph(f"{pdf_invoice_obj.customer.name}")),
        Row1(Paragraph("For our reference:", bold_style),
            Paragraph(f"{pdf_invoice_obj.reference_num}", normal_style), "",
            Paragraph(f"{pdf_invoice_obj.customer.address}")),
        Row1(Paragraph('Payment due:', bold_style),
            Paragraph(f"{pdf_invoice_obj.due}"), "",
            Paragraph(f"{pdf_invoice_obj.customer.postcode} {pdf_invoice_obj.customer.city}")),
        Row1("", "", "", Paragraph(f"{str(pdf_invoice_obj.customer.country).upper}")),
        Row1('', '', '', '')
    ]
    tbl2 = [
        Row2(Paragraph("Item", price_bold), 
            Paragraph("QTY", price_bold), 
            Paragraph("à (€)", price_bold),
            Paragraph("VAT 25% (€)", price_bold),
            Paragraph("Net (€)", price_bold), 
            Paragraph("Gross (€)", price_bold)),
    ]
    for itm in itms:
        rh[0].append(20)
        space -= 20
        nets.append(float(itm.net_total))
        taxes.append(float(itm.vat))
        grosses.append(float(itm.gross_total))
        tbl2.append(
            Row2(
            Paragraph(f"{itm.itm}", price_normal), 
            Paragraph(f"{itm.amount}", price_normal),
            Paragraph(f"{itm.net_per_one}", price_normal),
            Paragraph(f"{itm.vat}", price_normal),
            Paragraph(f"{itm.net_total}", price_normal), 
            Paragraph(f"{itm.gross_total}", price_normal)
            )
        )
    tbl2.append(
        Row2(
        Paragraph("Total:", price_bold), "", "",
        Paragraph(f"{sum(taxes)}", price_normal),
        Paragraph(f"{sum(nets)}", price_normal),
        Paragraph(f"{sum(grosses)}", price_bold))
    )
    summary = [
        [Paragraph(f"Total due by {pdf_invoice_obj.due}:", price_bold),
        Paragraph(f"{sum(grosses)}", price_normal)],
        [Paragraph("To account:", price_bold),
        Paragraph(f"{pdf_invoice_obj.creator.account}", price_normal)],
        [Paragraph("Use reference:", price_bold),
        Paragraph(f"{pdf_invoice_obj.invoice_num}", price_normal)]
    ]
    print(f"Rowheight: {rh}, space: {space}")
    tstyles = set_table_styles(tbl1, tbl2, rh)
    generate_pdf(inv_num, filename, vat_no, tstyles[0], tstyles[1], summary, space)

def set_table_styles(tbl, tbl_two, rowheights):
    """sets styling for tables in invoice

    Args:
        tbl (list): first table
        tbl_two (list): second table
        rowheights (list): rowheights for tbl_two based on number of items ordered

    Returns:
        tuple: styled tables
    """
    t = Table(tbl, colWidths=[110, 100, 150, 170], rowHeights=[40, 15, 15, 15, 40], vAlign='LEFT')
    t2 = Table(tbl_two, colWidths=[130, 70, 70, 70, 70, 70], rowHeights=rowheights[0], vAlign='LEFT')
    t2.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                           ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len = len(tbl_two)
    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey
        t2.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
    return t, t2
