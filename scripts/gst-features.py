"""Source text for the TaxPower GST features page (own wording; built by build-landing-pages.py)."""
GROUPS = [
('sales-returns', 'Sales returns: GSTR-1 and IFF', 'Prepare outward supply returns from your own records or imported data.', [
 ('Entering sales', ['B2B, B2C large and B2C small supplies', 'Exports, SEZ and deemed exports', 'Credit and debit notes and amendments', 'Nil-rated, exempt and non-GST supplies', 'HSN summary and documents issued', 'E-commerce supplies', 'Manual entry with GSTIN checks']),
 ('Bringing data in', ['Excel and JSON files', 'Tally data', 'E-invoice and e-way bill data']),
 ('Checking and filing', ['Download portal data and compare it with yours', 'Generate the JSON file and a draft PDF', 'File with EVC/OTP or DSC', 'Reset or delete portal data when needed', 'Move invoices of inactive or cancelled GSTINs', 'Compare GSTR-1 with GSTR-3B and PMT-06', 'GSTR-1A summary and PDF or Excel export'])]),
('summary-return', 'Monthly and quarterly summary: GSTR-3B', 'Build the summary return from your sales and purchase data and file it.', [
 ('Preparing the return', ['Section-wise entry for tables 3.1, 3.1.1, 3.2, 4, 5, 5.1 and 6.1', 'Fill from Excel, JSON or by hand', 'Auto-fill from GSTR-1', 'ITC worked out from GSTR-2B with a claim summary']),
 ('Reviewing', ['Compare with the portal return, GSTR-1, 2A and 2B', 'Set off tax from the cash and credit ledgers', 'Interest and liability breakup', 'Challan details for QRMP taxpayers']),
 ('Filing', ['Validate, create the JSON and file online', 'Draft and system-generated PDFs', 'Reports in PDF or Excel'])]),
('purchase-returns', 'Purchase data: GSTR-2A, 2B and 2', 'See what your suppliers have reported and what it means for your ITC.', [
 ('Downloading', ['Monthly, annual or several months at once', 'Supplier-wise and document-wise views', 'Filter, sort and search', 'Party-wise and ITC summaries']),
 ('Comparing', ['GSTR-2A against 2B and against GSTR-3B', 'Import your purchase register from Excel or JSON, including e-commerce purchases', 'ITC reversals', 'Purchase HSN summary and monthly reports'])]),
('supplier-invoices', 'Supplier invoices: IMS', 'Decide what happens to each invoice your suppliers have raised on you.', [
 ('Inward invoices', ['Download supplier invoices', 'Accept, reject or hold them in bulk', 'See supplies where ITC is reduced', 'GSTR-2B computed from your actions', 'Upload your actions from Excel']),
 ('Outward invoices and tracking', ['See what your customers did with your invoices', 'IMS dashboard', 'Error viewer', 'Purchase register against IMS'])]),
('annual-returns', 'Yearly returns: GSTR-9, 9A and 9C', 'Prepare the annual return and the reconciliation statement without starting from scratch.', [
 ('GSTR-9', ['Auto-populated from the year’s returns', 'Table 8A analysis and HSN summary', 'Table 7H reversals', 'Excel and JSON import', 'Comparison with source data', 'Draft PDF and online filing']),
 ('GSTR-9A', ['Prepare from Excel, JSON, the portal or by hand', 'Download from the portal and file']),
 ('GSTR-9C', ['Excel and JSON import', 'Audit validations and portal comparison', 'JSON generation, filing and PDF download'])]),
('composition', 'Composition dealers: CMP-08 and GSTR-4', 'Quarterly payments and the yearly return for composition taxpayers.', [
 ('CMP-08', ['Import from the portal or enter by hand', 'Interest, ledger check and challan creation', 'Payment, filing and a month-wise yearly report']),
 ('GSTR-4', ['Prepare from Excel, JSON or by hand', 'Download and reconcile GSTR-4A', 'Payment and filing'])]),
('other-returns', 'Other returns and forms', 'The less frequent returns are in the same software.', [
 ('Also available', ['GSTR-6 and 6A for input service distributors', 'GSTR-7 for TDS deductors', 'GSTR-8 for e-commerce operators', 'GSTR-10 final return', 'ITC-04 for job work', 'GSTR-2X for TDS and TCS credits', 'PMT-06 challans and self-assessment'])]),
('reconciliation', 'Reconciliation', 'Match your books with what the portal shows, with rules you control.', [
 ('Purchases', ['Purchase register against GSTR-2A, 2B and IMS', 'GSTR-2A against GSTR-2B', 'GSTR-2 against Table 8A and GSTR-4A', 'GSTR-6 against 6A']),
 ('Sales', ['Sales books against GSTR-1', 'GSTR-1 against e-invoice data', 'GSTR-1 against e-way bill data']),
 ('Matching controls', ['Adjustable matching and tolerance for small differences', 'Matching across periods', 'Include or exclude reverse charge', 'Remarks and several views', 'Export to Excel'])]),
('billing', 'Billing and accounts', 'Day-to-day invoicing that feeds your returns.', [
 ('Documents', ['Sales invoices, original and amended', 'Multi-rate invoices', 'Proforma invoices, quotations and sales orders', 'Delivery notes and bills of supply', 'Sales returns, credit and debit notes', 'Purchase invoices', 'Receipts and payments']),
 ('Set-up', ['Custom bill formats and fields', 'Masters for items, customers, suppliers and transporters', 'Account groups and ledgers', 'Invoice import from Excel']),
 ('Reports', ['Billing dashboard', 'Sales, purchase, receipt, ledger and group reports', 'Party summaries and activity log', 'Print or PDF'])]),
('e-invoicing', 'E-invoicing', 'Create invoice reference numbers from the same screen you bill from.', [
 ('Creating', ['IRN and signed QR for one invoice or many from Excel', 'Preview and validation', 'E-way bill created along with the e-invoice', 'Look up an e-way bill by IRN']),
 ('After creating', ['Cancel an IRN', 'Print in the prescribed format', 'Download e-invoices received', 'Reports and status tracking', 'Copy into GSTR-1'])]),
('e-way-bills', 'E-way bills', 'Handle the whole life of an e-way bill.', [
 ('Lifecycle', ['Generate singly or in bulk', 'Update Part-B and the transporter ID', 'Extend validity', 'Cancel or close']),
 ('Records', ['Download from the portal', 'Reports and party summary', 'Copy into GSTR-1'])]),
('clients-team', 'Client dashboards and team control', 'For practices that file for many clients.', [
 ('Dashboards', ['Filing status of every client', 'Return status across periods', 'Client turnover and profile', 'Due-date calendar', 'Interest and late fee calculator']),
 ('Clients and staff', ['Import clients from the portal or Excel', 'Client groups', 'Notes and reminders', 'Hide, lock or password-protect a client', 'User roles and client assignment', 'Audit trail'])]),
('notices', 'Notices and orders', 'Keep up with communication from the department.', [
 ('Handling notices', ['Download notices, orders and additional notices', 'Case details and attachments', 'One view of every client’s notices'])]),
('ledgers-payments', 'Ledgers, challans and payments', 'See balances and payments without leaving the software.', [
 ('Ledgers and statements', ['Electronic cash and credit ledgers', 'Liability register, parts I and II', 'Credit reversal and reclaim statement', 'Reverse charge liability and ITC statement', 'Negative liability statement']),
 ('Challans', ['Create, import and track challans', 'Download receipts', 'PMT-06 status'])]),
('refunds', 'Refunds and other applications', 'Apply for refunds and make voluntary payments.', [
 ('RFD-01', ['Exports, SEZ and deemed exports', 'Inverted duty structure', 'Excess balance or payment', 'Inter-state and intra-state corrections', 'Assessment, appeal and other cases', 'Annexure-B and supporting statements']),
 ('DRC-03', ['Voluntary payment with document upload'])]),
('reports', 'Reports and MIS', 'Review before and after filing.', [
 ('Summaries', ['GSTR-1 and GSTR-3B summaries by year, period and month', 'All-in-one summary', 'Interest summary']),
 ('Comparisons', ['GSTR-3B against GSTR-1, 2A, 2B and your books', 'Reverse charge tax against reverse charge ITC', 'Portal liability and ITC comparison', 'ITC matched and mismatched']),
 ('Parties and status', ['Party-wise summaries and supplier HSN details', 'Filing status of clients and suppliers', 'Export to Excel, PDF or Word, or send by email'])]),
('gstin-tools', 'GSTIN and HSN tools', 'Small checks that prevent big mistakes.', [
 ('Tools', ['Search a taxpayer by GSTIN', 'Validate many GSTINs together', 'Validate HSN codes', 'Check whether a supplier has filed', 'Auto-fill client profile', 'Import clients from the portal'])]),
('data-import', 'Importing your data', 'Start from what you already have.', [
 ('Sources', ['Tally Connector', 'One-click accounting import', 'Excel with your own column mapping', 'JSON files', 'Other GST software', 'Previous-year masters', 'Contacts from Excel', 'Client data import and export'])]),
('professional-tax', 'Professional Tax (Maharashtra)', 'For employers registered in Maharashtra.', [
 ('PTRC', ['Employer returns', 'Employee details', 'Challans']),
 ('PTEC', ['Enrolment certificate payments', 'Challans'])]),
('security-setup', 'Security, data and set-up', 'How the software keeps data safe and runs on your system.', [
 ('Portal access', ['Authorised GSP connection', 'GSP API usage view', 'Portal credentials stored per client', 'Password and OTP handling', 'Validation before submission']),
 ('Your data', ['SQL Server database in single-user or network mode', 'Offline preparation', 'Automatic backup and restore', 'PC and user management']),
 ('Upkeep', ['Error viewer', 'Automatic updates with a What’s New note'])]),
('support-extras', 'Support and extras', 'Help and small conveniences around the software.', [
 ('Help', ['Support tickets from inside the software', 'Online support and callbacks', 'Functional and technical support', 'Feedback option']),
 ('Extras', ['Referral programme', 'UDIN management', 'Email accounts and templates with a custom footer'])]),
]
FAQ = [
 ('Does TaxPower GST run online or on my computer?', 'It is desktop software for Windows. You install it on your system and connect it to the GST portal through an authorised GSP when you want to download data or file.'),
 ('Can I file returns without opening the GST portal?', 'Yes. You can upload and file with EVC/OTP or a DSC from inside the software. Portal data can also be downloaded for comparison before you file.'),
 ('Can I bring in data from Tally or Excel?', 'Yes. TaxPower GST imports from Tally using Tally Connector, from Excel with your own column mapping, and from JSON files or other GST software.'),
 ('I file for many clients. Is that supported?', 'Yes. A client dashboard shows the filing status of every client and period, with notes, reminders, user roles and password protection for client files.'),
 ('Is billing part of the same software?', 'GST billing is a separate module that works with the returns module. Invoices you create can flow into your returns, so the same data is not entered twice.'),
 ('Can I try it before buying?', 'Yes. Siddharth Enterprises can arrange a trial and a live demo, and help with installation and training in Marathi, Hindi or English.'),
 ('Who sells and supports TaxPower GST in Nagpur and Vidarbha?', 'Siddharth Enterprises, an authorised TaxPower dealer in Nagpur, handles demos, sales, installation and support. The software is developed by Magnum Infosystem.'),
]
