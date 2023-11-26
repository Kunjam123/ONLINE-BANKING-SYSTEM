import streamlit as st
import mysql.connector
from decimal import Decimal
from datetime import datetime, timedelta


# Establishing the connection to your MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysqlpswd',
    database='dbmp'
)

# Function to execute queries
def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result

###CUSTOMER

def get_last_customer_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(cust_id) FROM Customers")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0  # Return 0 if no customers exist

# Function to add a new customer
def add_customer(f_name, l_name, address, email, phone_number):
    last_id = get_last_customer_id()
    new_id = last_id + 1
    query = f"INSERT INTO Customers (cust_id, f_name, l_name, address, email, phone_number) VALUES ('{new_id}','{f_name}', '{l_name}', '{address}', '{email}', '{phone_number}')"
    execute_query(query)

# Function to display all customers
def display_all_customers():
    query = "SELECT * FROM Customers"
    result = execute_query(query)
    return result

# Function to display a singular customer
def display_customer(cust_id):
    query = f"SELECT * FROM Customers WHERE cust_id = {cust_id}"
    result = execute_query(query)
    return result

def customer_exists(customer_id):
    query = f"SELECT * FROM Customers WHERE cust_id = {customer_id}"
    result = execute_query(query)
    return len(result) > 0

# Function to delete customer and related loans
def delete_customer(customer_id):
    try:
        
        if customer_exists(customer_id):

            delete_transactions_query = f"DELETE FROM Transactions WHERE acc_id IN (SELECT acc_id FROM Accounts WHERE cust_id = {customer_id})"
            execute_query(delete_transactions_query)

            # Delete related loans
            delete_loans_query = f"DELETE FROM Loans WHERE cust_id = {customer_id}"
            execute_query(delete_loans_query)

            # Delete related loans
            delete_loans_query = f"DELETE FROM LoanPayment WHERE cust_id = {customer_id}"
            execute_query(delete_loans_query)


            # Delete related accounts
            delete_accounts_query = f"DELETE FROM Accounts WHERE cust_id = {customer_id}"
            execute_query(delete_accounts_query)

            # Delete customer
            delete_customer_query = f"DELETE FROM Customers WHERE cust_id = {customer_id}"
            execute_query(delete_customer_query)
        
            st.success(f"Customer ID {customer_id} deleted successfully along with related loans")
        else:
            st.error(f"Customer ID {customer_id} not found")
    except mysql.connector.Error as e:
        st.error(f"Error deleting customer: {e}")


# Streamlit app starts here
st.title('VINOD BANK')

st.title('Bank Management System')

# Add customer section
st.title('Customer')
# Display all customers section
st.header('Display All Customers')
customers = display_all_customers()
for customer in customers:
    st.write(customer)

# Add customer section
st.header('Add Customer')
f_name = st.text_input('First Name')
l_name = st.text_input('Last Name')
address = st.text_input('Address')
email = st.text_input('Email')
phone_number = st.text_input('Phone Number')
if st.button('Add Customer'):
    add_customer(f_name, l_name, address, email, phone_number)
    st.success('Customer added successfully!')

# Display singular customer section
st.header('Display Singular Customer')
cust_id = st.number_input('Enter Customer ID')
if st.button('Display Customer'):
    result = display_customer(cust_id)
    if result:
        st.write(result)
    else:
        st.write('Customer not found')

#delete
st.header('Customer Deletion')
del_cust_id = st.number_input('Customer ID to Delete', min_value=1)
if st.button('Delete Customer'):
    delete_customer(del_cust_id)



###BANK AND BRANCH

def get_last_bank_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(bank_id) FROM Bank")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0  # Return 0 if no customers exist


def add_bank(bank_code, bank_address, name):
    last_id = get_last_bank_id()
    new_id = last_id + 1
    query = f"INSERT INTO Bank (bank_id, bank_code, bank_address, name) VALUES ('{new_id}', '{bank_code}', '{bank_address}', '{name}')"
    execute_query(query)

# Function to display all banks
def display_all_banks():
    query = "SELECT * FROM Bank"
    result = execute_query(query)
    return result

# Function to fetch and display bank details by bank ID
def display_bank(bank_id):
    try:
        query = f"SELECT * FROM Bank WHERE bank_id = {bank_id}"
        result = execute_query(query)
        
        if len(result) > 0:
            st.write(f"Bank ID: {result[0][0]}")
            st.write(f"Bank Code: {result[0][1]}")
            st.write(f"Bank Address: {result[0][2]}")
            st.write(f"Bank Name: {result[0][3]}")
        else:
            st.error(f"Bank ID {bank_id} not found")
    except mysql.connector.Error as e:
        st.error(f"Error fetching bank details: {e}")


# Function to add a new branch
def add_branch(branch_no, branch_name, branch_address, bank_id):
    query = f"INSERT INTO Branch (branch_no, branch_name, branch_address, bank_id) VALUES ('{branch_no}', '{branch_name}', '{branch_address}', {bank_id})"
    execute_query(query)

# Function to display all branches
def display_all_branches():
    query = "SELECT * FROM Branch"
    result = execute_query(query)
    return result

# Function to fetch and display branch details by branch ID
def display_branch(branch_id):
    try:
        query = f"SELECT * FROM Branch WHERE branch_no = {branch_id}"
        result = execute_query(query)
        
        if len(result) > 0:
            st.write(f"Branch No.: {result[0][0]}")
            st.write(f"Branch Name: {result[0][1]}")
            st.write(f"Branch Address: {result[0][2]}")
            st.write(f"Bank ID: {result[0][3]}")
        else:
            st.error(f"Branch ID {branch_id} not found")
    except mysql.connector.Error as e:
        st.error(f"Error fetching branch details: {e}")

# Streamlit app starts here

st.title('Bank and Branch')
# Display all Banks section
st.header('Display All Banks')
banks = display_all_banks()
for bank in banks:
    st.write(bank)

# Add Bank section
st.header('Add Bank')
#bank_id = st.number_input('Bank ID', min_value=1)
bank_code = st.number_input('Bank Code', min_value=1)
bank_address = st.text_input('Bank Address')
name = st.text_input('Bank Name')

if st.button('Add Bank'):
    add_bank(bank_code, bank_address, name)
    st.success('Bank added successfully!')

st.header('Display Bank by ID')

# Display Bank section
bank_id = st.number_input('Enter Bank ID', min_value=1)
if st.button('Display Bank'):
    display_bank(bank_id)

# Display all Branches section
st.header('Display All Branches')
branches = display_all_branches()
for branch in branches:
    st.write(branch)

# Add Branch section
st.header('Add Branch')
branch_no = st.number_input('Branch Number', min_value=1)
branch_name = st.text_input('Branch Name')
branch_address = st.text_input('Branch Address')
bank_id_branch = st.number_input('Bank ID')

if st.button('Add Branch'):
    add_branch(branch_no, branch_name, branch_address, bank_id_branch)
    st.success('Branch added successfully!')

st.header('Display Branch by ID')
# Display Branch section
branch_id = st.number_input('Enter Branch ID', min_value=1)
if st.button('Display Branch'):
    display_branch(branch_id)


###ACCOUNT

def get_last_account_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(acc_id) FROM Accounts")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0

# Function to add a new account
def add_account(acc_no, acc_type, date, balance, cust_id, brn_no):
    last_id = get_last_account_id()
    new_id = last_id + 1
    query = f"INSERT INTO Accounts (acc_no, acc_id, type, date, balance, cust_id, branch_no) VALUES ({acc_no}, {new_id}, '{acc_type}', '{date}', {balance}, {cust_id}, {brn_no})"
    execute_query(query)

def account_exists(account_number, account_id):
    try:
        query = f"SELECT * FROM Accounts WHERE acc_no = {account_number} AND acc_id = {account_id}"
        result = execute_query(query)
        return len(result) > 0
    except mysql.connector.Error as e:
        st.error(f"Error checking account: {e}")

# Function to delete the account
def delete_account(account_number, account_id):
    try:
        if account_exists(account_number, account_id):
            delete_query = f"DELETE FROM Accounts WHERE acc_no = {account_number} AND acc_id = {account_id}"
            execute_query(delete_query)
            st.success(f"Account Number {account_number} with Account ID {account_id} deleted successfully")
        else:
            st.error(f"Account Number {account_number} with Account ID {account_id} not found")
    except mysql.connector.Error as e:
        st.error(f"Error deleting account: {e}")

# Function to display all accounts
def display_all_accounts():
    query = "SELECT * FROM Accounts"
    result = execute_query(query)
    return result

# Function to fetch and display account details by account number and ID
def display_account(acc_number, acc_id):
    try:
        query = f"SELECT * FROM Accounts WHERE acc_no = {acc_number} AND acc_id = {acc_id}"
        result = execute_query(query)
        
        if len(result) > 0:
            st.write(f"Account Number: {result[0][0]}")
            st.write(f"Account ID: {result[0][1]}")
            st.write(f"Account Type: {result[0][2]}")
            st.write(f"Date: {result[0][3]}")
            st.write(f"Balance: {result[0][4]}")
            st.write(f"Customer ID: {result[0][5]}")
            st.write(f"Branch Number: {result[0][6]}")
        else:
            st.error(f"Account Number {acc_number} with Account ID {acc_id} not found")
    except mysql.connector.Error as e:
        st.error(f"Error fetching account details: {e}")

# Streamlit app starts here
st.title('Account Management')

# Display all Accounts section
st.header('Display All Accounts')
accounts = display_all_accounts()
for account in accounts:
    st.write(account)

# Add Account section
st.header('Add Account')
acc_no = st.number_input('Account Number', min_value=1)
#acc_id = st.number_input('Account ID', min_value=1)
acc_type = st.selectbox('Account Type', ['Savings', 'Checking', 'Investment'])
date = st.date_input('Date')
balance = st.number_input('Balance', min_value=0.0)
cust_id = st.number_input('Customer ID', min_value=1)
brn_no = st.number_input('BranchNumber', min_value=1)

if st.button('Add Account'):
    add_account(acc_no, acc_type, date, balance, cust_id, brn_no)
    st.success('Account added successfully!')

# Display Account section
st.header('Display Account by Number and ID')
acc_number = st.number_input('Enter Account Number', min_value=1)
acc_id = st.number_input('Enter Account ID', min_value=1)
if st.button('Display Account'):
    display_account(acc_number, acc_id)

# Delete Account section
st.header('Delete Account')
del_acc_no = st.number_input('Account Number to Delete', min_value=1)
del_acc_id = st.number_input('Account ID to Delete', min_value=1)

if st.button('Delete Account'):
    delete_account(del_acc_no, del_acc_id)
    #st.success('Account deleted successfully!')


###TRANSACTIONS


def get_last_transaction_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(id) FROM Transactions")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0  # Return 0 if no Transactions exist


# Function to add a new customer
def add_transaction(type, amount, acc_id):
    last_id = get_last_transaction_id()
    new_id = last_id + 1
    query = f"INSERT INTO Transactions (id, type, amount, acc_id) VALUES ('{new_id}','{type}', '{amount}', '{acc_id}')"
    if transaction_type == 'Deposit':
        update_balance_query = f"UPDATE Accounts SET balance = balance + {amount} WHERE acc_id = {acc_id}"
    elif transaction_type == 'Withdrwal':
        update_balance_query = f"UPDATE Accounts SET balance = balance - {amount} WHERE acc_id = {acc_id}"
    execute_query(update_balance_query)

    execute_query(query)

# Function to display all Transactions
def display_all_Transactions():
    query = "SELECT * FROM Transactions"
    result = execute_query(query)
    return result

# Function to display all accounts with balances
def display_all_accounts_with_balance():
    query = "SELECT acc_id, acc_no, balance FROM Accounts"
    result = execute_query(query)
    return result

# Streamlit app starts here
st.title('Transaction and Loan Management')

# Display all Transactions section
st.header('Display All Transactions')
transactions = display_all_Transactions()
for transaction in transactions:
    st.write(transaction)

# Add Transaction section
st.header('Add Transaction')
#transaction_id = st.number_input('Transaction ID', min_value=1)
transaction_type = st.selectbox('Transaction Type', ['Withdrwal', 'Deposit'])
amount = st.number_input('Amount', min_value=0.0)
acc_id = st.number_input('Account ID')

if st.button('Add Transaction'):
    add_transaction(transaction_type, amount, acc_id)
    st.success('Transaction added successfully!')

# Display all Accounts with balances section
st.header('Display All Accounts with Balances')
accounts = display_all_accounts_with_balance()
for account in accounts:
    st.write(account)

 
##LOANS

def get_last_loan_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(loan_id) FROM loans")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0  # Return 0 if no loans exist


# Function to add loan
'''def add_loan(type, loan_amount, cust_id, branch_no):
    last_id = get_last_loan_id()
    new_id = last_id + 1
    query = f"INSERT INTO loans (loan_id, type, loan_amount, cust_id, branch_no) VALUES ('{new_id}','{type}', '{loan_amount}', '{cust_id}','{branch_no}')"
    execute_query(query)'''

def add_loan(type, loan_amount, cust_id, branch_no):
    last_id = get_last_loan_id()
    new_id = last_id + 1
    # Set dates
    current_date = datetime.now().date()
    repayment_date = current_date + timedelta(days=365)  # A year later

    query = f"INSERT INTO Loans (loan_id, type, loan_amount, status, date_of_loan, repayment_due, cust_id, branch_no)" \
    f"VALUES ('{new_id}','{type}', '{loan_amount}', 'Pending', '{current_date}', '{repayment_date}', '{cust_id}', '{branch_no}')"
    execute_query(query)

# Function to display all loans
def display_all_loans():
    query = "SELECT * FROM loans"
    result = execute_query(query)
    return result

def get_last_loanpy_id():
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT MAX(payment_id) FROM LoanPayment")
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id if last_id else 0 

# Function to pay loan and update status
'''def pay_loan(loan_id, cust_id, date, amount_paid):
    last_id = get_last_loanpy_id()
    new_id = last_id + 1
    try:
        # Fetch current loan amount and status
        query = "SELECT loan_amount, status FROM Loans WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
        loan_info = execute_query(query)
        
        if len(loan_info) > 0:
            current_loan_amount, status = loan_info[0]
            
            amount_paid_decimal = Decimal(str(amount_paid))
            
            # Update loan amount after payment
            new_loan_amount = max(current_loan_amount - amount_paid_decimal, Decimal('0.00'))  # Ensure the loan amount doesn't go below zero


            # Update status based on the remaining amount
            new_status = 'paid' if new_loan_amount == Decimal('0.00') else 'pending'

            # Update the loan amount and status in the Loans table
            #update_query = "UPDATE Loans SET loan_amount = %s, status = %s WHERE loan_id = %s" % (new_loan_amount, new_status, loan_id)
            #update_query=f"UPDATE Loans (loan_amount, status, loan_id) VALUES ('{new_loan_amount}','{new_status}', '{loan_id}')"
            #execute_query(update_query)
            #print(result)
            inf = "SELECT repayment_due FROM Loans WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
            rep = execute_query(inf)

            update_query = f"UPDATE Loans SET loan_amount = {new_loan_amount}, status = '{new_status}' WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
            execute_query(update_query)
            loanpy_query = f"UPDATE LoanPayment SET payment_id = {new_id}, date_of_repayment = {date}, repayment_due = {rep}  WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
            execute_query(loanpy_query)
            st.success(f"Loan ID {loan_id} payment processed. New loan amount: {new_loan_amount}. Loan status: {new_status}")
        else:
            st.error("Loan ID not found")
    except mysql.connector.Error as e:
        st.error(f"Error paying loan: {e}")'''

def pay_loan(loan_id, cust_id, date, amount_paid):
    try:
        last_id = get_last_loanpy_id()
        new_id = last_id + 1
        query_loan = f"SELECT loan_amount, status, repayment_due FROM Loans WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
        loan_info = execute_query(query_loan)
        
        if len(loan_info) > 0:
            current_loan_amount, status, repayment_due = loan_info[0]

            amount_paid_decimal = Decimal(str(amount_paid))
            new_loan_amount = max(current_loan_amount - amount_paid_decimal, Decimal('0.00'))

            new_status = 'paid' if new_loan_amount == Decimal('0.00') else 'pending'

            mycursor = conn.cursor()
            inf = f"SELECT repayment_due FROM Loans WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
            mycursor.execute(inf)
            # Fetch the result
            rep = mycursor.fetchone()

            # Update loan amount and status in the Loans table
            update_query_loan = f"UPDATE Loans SET loan_amount = {new_loan_amount}, status = '{new_status}' WHERE loan_id = {loan_id} AND cust_id = {cust_id}"
            execute_query(update_query_loan)

            # Update LoanPayment table
            penalty_query = f"INSERT INTO LoanPayment (payment_id, date_of_repayment, amount_paid, repayment_due, cust_id, loan_id) VALUES ('{new_id}', '{date}', '{amount_paid}', '{rep}', {cust_id}, {loan_id})"
            execute_query(penalty_query)

            st.success(f"Loan ID {loan_id} payment processed. New loan amount: {new_loan_amount}. Loan status: {new_status}")
        else:
            st.error("Loan ID not found")
    except mysql.connector.Error as e:
        st.error(f"Error paying loan: {e}")


# Display all Loans section
st.header('Display All Loans')
loans = display_all_loans()
for loan in loans:
    st.write(loan)

# Add Loan section
st.header('Take a Loan')
#loan_id = st.number_input('Loan ID', min_value=1)
loan_type = st.selectbox('Loan Type', ['Personal', 'Mortgage', 'Auto', 'Student'])
loan_amount = st.number_input('Loan Amount', min_value=0.0)
cust_id_loan = st.number_input('Customer ID')
branch_no_loan = st.number_input('Branch Number')

if st.button('Take Loan'):
    add_loan(loan_type, loan_amount, cust_id_loan, branch_no_loan)
    st.success('Loan added successfully!')

# Pay Loan section
st.header('Pay Loan')
loan_id = st.number_input('Loan ID', min_value=1)
cust_id = st.number_input('Cust ID', min_value=1)
date_py = st.date_input('Payment Date')
amount_paid = st.number_input('Amount Paid', min_value=0.0)

if st.button('Pay Loan'):
    pay_loan(loan_id, cust_id, date_py, amount_paid)
    st.success('Payment made successfully!')

# Close the connection to the database
conn.close()