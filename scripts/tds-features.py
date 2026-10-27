"""Source text for the TaxPower TDS features page (own wording; built by build-landing-pages.py)."""
GROUPS = [
('tds-returns', 'TDS and TCS returns: 24Q, 26Q, 27Q, 27EQ', 'One workspace for each kind of statement, original or correction.', [
 ('Statements', ['24Q for salary, with the annual salary details', '26Q for payments to residents', '27Q for payments to non-residents', '27EQ for tax collected at source', 'Original and correction statements', 'Earlier years and quarters']),
 ('Working in it', ['Separate screen for every statement type', 'Summary before you generate the file', 'Due date and filing date on each statement', 'Status from preparation to processing', 'Earlier filing details alongside', 'Any number of TANs in the edition you buy']),
 ('Entering data', ['Deduction entry with deductee and section pick-lists', 'Import from Excel, text files and consolidated statements', 'Deductee and section details tied to challans'])]),
('new-act', 'Income-tax Act 2025 forms', 'New form numbers and the new filing tools, handled in the same screens.', [
 ('New forms', ['Form 138 in place of 24Q', 'Form 140 in place of 26Q', 'Form 144 in place of 27Q', 'Form 143 in place of 27EQ']),
 ('Supporting tools', ['Current FVU and RPU versions', 'New portal and TRACES steps'])]),
('validation', 'Checks, pre-scrutiny and FVU', 'Catch the mistakes before the department does.', [
 ('Before filing', ['Many built-in checks on the statement data', 'Pre-scrutiny pass', 'PAN review for every deductee', 'Tax shortfall, interest and fee checks']),
 ('FVU', ['File validation utility run from inside the software', 'Open the FVU statement, error file and warning file in one click', 'Open the FVU folder directly', 'Error messages in plain view', 'Fix and generate again', 'Readiness shown for each statement'])]),
('e-filing', 'Filing online', 'Send the statement from the same screen where you prepared it.', [
 ('Submitting', ['Direct filing with OTP verification', 'Deductor login to the income-tax portal', 'Form 27A made automatically', 'Fresh submission and resubmission']),
 ('Afterwards', ['Acknowledgement number', 'RRR number', 'Processing status in the return register']),
 ('Online activities', ['Open Form 27A as PDF', 'View the acknowledgement', 'Log in to the income-tax portal from here', 'Log in to TRACES from here', 'Validate PAN and TDS certificates from the same list'])]),
('traces', 'TRACES in the same software', 'Request, download and read what TRACES sends back.', [
 ('Requests and downloads', ['TRACES login saved for each deductor', 'Consolidated statement requests', 'Justification reports for the consolidated file', 'Form 16 and Form 16A downloads', 'Outstanding demand and challan details', 'TRACES inbox and a list of your requests']),
 ('Less manual work', ['Token picked up automatically', 'Consolidated and CSI files handled for you', 'Downloaded files verified', 'Section 200A intimations read', 'Default summary checks'])]),
('corrections', 'Correction statements', 'Fix a filed statement without starting over.', [
 ('Preparing', ['Correction built from the downloaded consolidated file', 'Justification report review to find defaults', 'Current and earlier periods']),
 ('Tracking', ['Every original and correction in one history', 'Acknowledgement and status after each revision'])]),
('challans', 'Challans and payments', 'Keep payments and deductions matched.', [
 ('Getting challans in', ['Download challans from the income-tax portal', 'Download challans from TRACES', 'Fetch book-entry details with BIN from NSDL', 'Import from OLTAS or earlier periods', 'Create challans from your own deduction entries']),
 ('Challans', ['Add and edit with CIN update', 'Pay through the income-tax portal', 'BIN check for book-entry payments', 'PDF receipts']),
 ('Matching', ['Automatic deduction-to-challan mapping', 'Unused balance put to use', 'Claim handling', 'Consolidated challan view', 'Payment and liability reconciliation'])]),
('computation', 'Interest, fees and liability', 'Know what you owe before the notice does.', [
 ('Calculations', ['Interest for late deduction and late payment', 'Late filing fee under section 234E', 'Penalty computation']),
 ('Breakups', ['By deductee and section', 'By quarter and by year', 'Challan use and tax liability'])]),
('deductors', 'Deductors and TANs', 'Every client or branch set up once.', [
 ('Records', ['TAN, profile and responsible person', 'Groups and classes of deductors', 'Import and export of deductors']),
 ('Access', ['Portal and TRACES logins stored securely', 'Dashboard for every deductor and TAN'])]),
('deductees', 'Deductees, employees and PAN', 'Clean masters mean fewer defaults.', [
 ('Masters', ['Deductee and employee masters', 'Employee salary details', 'Bulk import of both from Excel', 'Deduction details linked to each person']),
 ('PAN and certificates', ['Quick check of a single PAN', 'Bulk PAN validation for the whole list', 'Validation results saved against each deductee', 'PAN update workflow', 'Higher-rate checks for missing PAN', 'Validate TDS certificates against the records', 'Section 197 certificate check with mismatches flagged'])]),
('certificates', 'Form 16, 16A and 27D', 'Certificates ready to hand over.', [
 ('Certificates', ['Form 16 parts A and B for employees', 'Form 16A for other deductions, from TRACES', 'Form 27D for tax collected']),
 ('Delivery', ['Certificate validation before you send', 'Digital signing', 'Preview, print or save as PDF', 'Send by email to employees and deductees'])]),
('compliance', 'Compliance checks', 'See likely defaults while there is still time to act.', [
 ('Prediction', ['Likely defaults before you submit', 'Invalid PAN, short deduction, challan mismatch and interest flags']),
 ('Overview', ['Checks by deductee and by section', 'One dashboard for every open issue', 'Status and timely alerts'])]),
('tds-reports', 'Reports', 'Registers and statements you can print or export.', [
 ('Registers', ['Return register with filing and processing status', 'Challan register', 'Tax deduction register']),
 ('Statements', ['Monthly deduction summary', 'Deductee-wise statement by quarter and year', 'Section-wise statement', 'Employee summaries and salary reports', 'Interest and compliance reports', 'Support for Form 3CD (beta)', 'Excel and PDF export'])]),
('tds-platform', 'Users, data and set-up', 'Run it for one desk or a whole office.', [
 ('Team', ['Users with role-based access', 'Email account for certificates and reports', 'Preferences and settings']),
 ('Data', ['Fast database', 'Single computer, or several over LAN, WAN, VPN or a Windows VPS', 'Backup and restore', 'Software updates', 'Client data kept protected'])]),
('tds-help', 'Help and guidance', 'People and prompts when you are stuck.', [
 ('Help', ['Help and notifications inside the software', 'Online onboarding and training', 'Remote assistance for supported tasks', 'Guidance when filing rules change'])]),
]

FAQ = [
('Which TDS forms can TaxPower TDS prepare?', 'It prepares 24Q, 26Q, 27Q and 27EQ returns, and the matching Form 138, 140, 144 and 143 under the Income-tax Act 2025, along with correction returns for them.'),
('Can I file correction returns?', 'Yes. Request the consolidated file and justification report from TRACES, and TaxPower helps you prepare the correction from them.'),
('Can I bring deductee data from Excel?', 'Yes. Deductee, employee and challan details can be imported from Excel or text files, and the PAN list can be validated in bulk or one PAN at a time.'),
('Can I download challans instead of typing them?', 'Yes. Challans can be downloaded from the income-tax portal and TRACES, book-entry details fetched with the BIN, or challans created from your own deduction entries.'),
('Does it generate Form 16 and 16A?', 'Yes. Form 16 is prepared for salaried employees, Form 16A comes from TRACES, and Form 27D covers tax collected at source. You can sign, print and email them.'),
('Can I file the return from inside the software?', 'Yes. It runs the file validation utility, creates Form 27A and files with OTP verification. The acknowledgement and RRR numbers are saved with the return.'),
('Will someone help me install and learn it?', 'Siddharth Enterprises, the authorized dealer in Nagpur, helps with installation, training and support in Marathi, Hindi and English.'),
]
