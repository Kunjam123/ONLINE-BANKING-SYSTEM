CREATE TABLE Customers (
    cust_id INT PRIMARY KEY NOT NULL,
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    address VARCHAR(255) DEFAULT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20)
);

DELIMITER //
CREATE TRIGGER before_customer_insert
BEFORE INSERT ON Customers
FOR EACH ROW
BEGIN
    IF CHAR_LENGTH(NEW.phone_number) != 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phone number must be 10 digits';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER before_emailcustomer_insert
BEFORE INSERT ON Customers
FOR EACH ROW
BEGIN
    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END;
//
DELIMITER ;


CREATE TABLE Bank (
    bank_id INT NOT NULL,
    bank_code INT NOT NULL,
    bank_address VARCHAR(255),
    PRIMARY KEY (bank_id, bank_code),
    name VARCHAR(100)
);

CREATE TABLE Branch (
    branch_no INT PRIMARY KEY NOT NULL,
    branch_name VARCHAR(100),
    branch_address VARCHAR(255),
    bank_id INT,
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id)
);

CREATE TABLE Accounts (
    acc_no INT NOT NULL,
    acc_id INT NOT NULL,
    type ENUM('Savings', 'Checking', 'Investment') DEFAULT 'Checking',
    date DATE,
    balance DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (acc_id, acc_no),
    cust_id INT,
    branch_no INT,
    FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
    FOREIGN KEY (branch_no) REFERENCES Branch(branch_no)
);

DELIMITER //
CREATE TRIGGER check_initial_balance
BEFORE INSERT ON Accounts
FOR EACH ROW
BEGIN
    IF NEW.balance <= 5000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Initial balance cannot be less than 5000';
    END IF;
END;
//
DELIMITER ;


CREATE TABLE Transactions (
    id INT PRIMARY KEY,
    type ENUM('Withdrwal','Deposit') NOT NULL,
    amount DECIMAL(15, 2),
    acc_id INT,
    FOREIGN KEY (acc_id) REFERENCES Accounts(acc_id)
);

DELIMITER //
CREATE TRIGGER check_balance 
BEFORE INSERT ON Transactions 
FOR EACH ROW
BEGIN
    DECLARE current_balance DECIMAL(15, 2);
    
    SELECT balance INTO current_balance
    FROM Accounts
    WHERE acc_id = NEW.acc_id;

    IF NEW.type = 'Withdrawal' THEN
        IF (current_balance - NEW.amount) < 5000 AND current_balance >= 5000 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Transaction rejected: Insufficient balance';
        ELSEIF NEW.amount > current_balance THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Transaction rejected: Insufficient balance';
        END IF;
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER prevent_zero_transaction
BEFORE INSERT ON Transactions
FOR EACH ROW
BEGIN
    IF NEW.amount <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Amount cannot be 0';
    END IF;
END;
//
DELIMITER ;

/*CREATE TABLE Loans (
    loan_id INT PRIMARY KEY,
    type ENUM('Personal', 'Mortgage', 'Auto', 'Student') DEFAULT 'Personal',
    loan_amount DECIMAL(15, 2),
    status VARCHAR(50),
    cust_id INT,
    branch_no INT,
    FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
    FOREIGN KEY (branch_no) REFERENCES Branch(branch_no)
);*/

CREATE TABLE Loans (
    loan_id INT NOT NULL,
    type ENUM('Personal', 'Mortgage', 'Auto', 'Student') DEFAULT 'Personal',
    loan_amount DECIMAL(15, 2),
    status VARCHAR(50),
    date_of_loan DATE NOT NULL,
    repayment_due DATE,
    PRIMARY KEY (loan_id, repayment_due),
    cust_id INT,
    branch_no INT,
    FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
    FOREIGN KEY (branch_no) REFERENCES Branch(branch_no)
);

CREATE TABLE LoanPayment(
    payment_id INT PRIMARY KEY,
    date_of_repayment DATE NOT NULL,
    amount_paid DECIMAL(15, 2) NOT NULL,
    penalty DECIMAL(15, 2) DEFAULT 0,
    repayment_due DATE,
    cust_id INT,
    loan_id INT,
    FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
    FOREIGN KEY (loan_id) REFERENCES Loans(loan_id)
);

DELIMITER //
CREATE TRIGGER prevent_zero_loan
BEFORE INSERT ON Loans
FOR EACH ROW
BEGIN
    IF NEW.loan_amount = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Loan amount cannot be 0';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER check_repayment_date
BEFORE INSERT ON LoanPayment 
FOR EACH ROW
BEGIN
    DECLARE specified_date DATE;
    DECLARE lamt DECIMAL(15, 2);

    SELECT repayment_due, loan_amount INTO specified_date, lamt 
    FROM Loans 
    WHERE loan_id = NEW.loan_id;

    IF NEW.date_of_repayment > specified_date THEN
        SET NEW.penalty = (7/100) * lamt;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Repayment date exceeds specified date. Penalty applied.';
    END IF;
END;
//
DELIMITER ;



INSERT INTO Customers (cust_id, f_name, l_name, address, email, phone_number)
VALUES (1, 'ABC', 'BCA', '123 Main Road', 'abc@gmail.com', '1234567890'),
       (2, 'DEF', 'FED', '456 Main Road', 'def@gmail.com', '9876543210');

INSERT INTO Bank (bank_id, bank_code, bank_address, name)
VALUES (1, 1001, 'Bangalore', 'Bank1'), 
       (2, 1002, 'Bangalore', 'Bank2'); 

INSERT INTO Branch (branch_no, branch_name, branch_address, bank_id)
VALUES (1, 'Main Branch', 'Jayanagar, Bangalore', 1),
       (2, 'Downtown Branch', 'Kalyanagar, Bangalore', 1);

INSERT INTO Accounts (acc_no, acc_id, type, date, balance, cust_id, branch_no)
VALUES (1001, 1, 'Savings', '2023-07-22', 15000.00, 1, 2 ),
       (1002, 2, 'Checking', '2023-08-04', 10000.00, 2, 1);

INSERT INTO Transactions (id, type, amount, acc_id)
VALUES (1, 'Deposit', 1000.00, 1), 
       (2, 'Withdrwal', 500.00, 2); 

INSERT INTO Loans (loan_id, type, loan_amount, status, date_of_loan, repayment_due, cust_id, branch_no)
VALUES (1, 'Personal', 20000, 'Pending', '2022-05-27', '2023-05-27', 1, 1), 
       (2, 'Mortgage', 50000, 'Paid', '2023-03-15', '2024-03-15', 2, 2);

INSERT INTO LoanPayment (payment_id, date_of_repayment, amount_paid, repayment_due, cust_id, loan_id)
VALUES (1, '2023-04-15', 5000, '2023-05-27', 1,1),
       (2, '2023-09-02', 10000, '2024-03-15', 2, 2);


