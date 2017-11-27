import os

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
os.environ["INVOICE_LANG"] = "en"

client = Client('Nishutosh Sharma')
provider = Provider('Fashvolts', bank_account='2600420569/2010')
creator = Creator('Ankit')

invoice = Invoice(client, provider, creator)


invoice.currency=u'Rs.'
invoice.add_item(Item(32, 600, description="Item 1"))
invoice.add_item(Item(60, 50, description="Item 2", tax=10))
invoice.add_item(Item(50, 60, description="Item 3", tax=5))
invoice.add_item(Item(5, 600, description="Item 4", tax=50))

pdf = SimpleInvoice(invoice)
pdf.gen("invoice.pdf", generate_qr_code=False)
