DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    full_name NVARCHAR(200),
    email NVARCHAR(200),
    phone NVARCHAR(50),
    address NVARCHAR(300)
);

INSERT INTO customers (customer_id, full_name, email, phone, address)
VALUES (1, 'Jon Smith', 'jsmith@gmail.com', '555-123-4567', '12 Elm St');

INSERT INTO customers (customer_id, full_name, email, phone, address)
VALUES (2, 'Maria Garcia', 'mgarcia@yahoo.com', '555-987-6543', '88 Oak Ave');

SELECT * FROM customers;
GO
