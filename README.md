# E-Commerce Payment Transaction Analysis & Simulation

A data-driven e-commerce payment transaction project built using **Python, MySQL, SQL, and Streamlit**.

The project simulates payment transactions, stores transactional data in a relational MySQL database, and performs SQL-based analysis to identify customer, order, product, and payment trends.

---

## Project Overview

This project is designed to demonstrate how transactional e-commerce data can be managed, analysed, and simulated using Python and SQL.

The project contains four relational datasets:

- Users
- Products
- Orders
- Transactions

Historical transaction data is analysed using SQL, while Python is used to simulate new payment transactions and store them in MySQL.

A Streamlit interface provides an interactive way to demonstrate the payment simulation and transaction history.

---

## Objectives

- Analyse e-commerce customer and transaction data.
- Understand payment method performance.
- Analyse successful, failed, pending, and refunded transactions.
- Identify high-value customers and products.
- Analyse monthly revenue and transaction trends.
- Demonstrate relational database operations using MySQL.
- Simulate new payment transactions using Python.
- Provide an interactive Streamlit interface for demonstration.

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Payment simulation and application logic |
| MySQL | Relational database management |
| SQL | Data analysis and business insights |
| Streamlit | Interactive application interface |
| Pandas | Data handling and analysis |

---

## Dataset

The project uses four related tables.

### 1. Users

Contains customer information such as:

- User ID
- Name
- Email
- Phone
- Age
- Gender
- City
- State
- Customer Type
- Signup Date

### 2. Products

Contains product information:

- Product ID
- Product Name
- Category
- Unit Price
- Stock

### 3. Orders

Contains order-level information:

- Order ID
- User ID
- Product ID
- Order Date
- Quantity
- Unit Price
- Discount
- Total Amount
- Order Status

### 4. Transactions

Contains payment information:

- Transaction ID
- Order ID
- User ID
- Transaction Date
- Payment Method
- Amount
- Transaction Status
- Transaction Reference

---

## Dataset Size

The dataset contains approximately:

- **5,000 Users**
- **500 Products**
- **20,000 Orders**
- **20,000 Transactions**

The data is designed for analytical and simulation purposes.

---

## Database Relationship

```text
Users
  |
  | user_id
  |
  v
Orders
  |
  | order_id
  |
  v
Transactions

Products
  |
  | product_id
  |
  v
Orders
