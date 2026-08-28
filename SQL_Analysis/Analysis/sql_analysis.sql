create database Ecommerce;
use Ecommerce;
show tables;

set SQL_SAFE_UPDATES = 0;
set SQL_SAFE_UPDATES = 1;
select*from users;

-- data quality
SELECT 'users' AS table_name, COUNT(*) AS total_records
FROM users
UNION ALL
SELECT 'products', COUNT(*)
FROM products
UNION ALL
SELECT 'orders', COUNT(*)
FROM orders
UNION ALL
SELECT 'transactions', COUNT(*)
FROM transactions;

-- Check Null value across the tables
SELECT
    COUNT(*) AS total_users,
    SUM(name IS NULL) AS null_names,
    SUM(email IS NULL) AS null_emails,
    SUM(phone IS NULL) AS null_phones
FROM users;

SELECT
    COUNT(*) AS total_orders,
    SUM(user_id IS NULL) AS null_user_id,
    SUM(product_id IS NULL) AS null_product_id,
    SUM(total_amount IS NULL) AS null_amount
FROM orders;

SELECT
    COUNT(*) AS total_transactions,
    SUM(order_id IS NULL) AS null_order_id,
    SUM(amount IS NULL) AS null_amount
FROM transactions;

-- Customer type distribution
SELECT
    customer_type,
    COUNT(*) AS total_customers
FROM users
GROUP BY customer_type
ORDER BY total_customers DESC;

-- Top 10 customer by spending
SELECT
    u.user_id,
    u.name,
    u.customer_type,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM users u
JOIN orders o
    ON u.user_id = o.user_id
WHERE o.order_status = 'Completed'
GROUP BY
    u.user_id,
    u.name,
    u.customer_type
ORDER BY total_spent DESC
LIMIT 10;

-- Average spending by customer type
SELECT
    u.customer_type,
    COUNT(DISTINCT u.user_id) AS customers,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM users u
JOIN orders o
    ON u.user_id = o.user_id
WHERE o.order_status = 'Completed'
GROUP BY u.customer_type
ORDER BY total_revenue DESC;

-- Order status distribution
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders),
        2
    ) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- Revenue by oder status
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_amount
FROM orders
GROUP BY order_status
ORDER BY total_amount DESC;

-- Monthly revenue
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_amount), 2) AS revenue
FROM orders
WHERE order_status = 'Completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- Payment method performance
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS average_transaction
FROM transactions
GROUP BY payment_method
ORDER BY total_amount DESC;

-- Payment status
SELECT
    transaction_status,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY transaction_status
ORDER BY total_transactions DESC;

-- Payment sucess rate
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(
        CASE
            WHEN transaction_status = 'Success'
            THEN 1
            ELSE 0
        END
    ) AS successful_transactions,

    ROUND(
        SUM(
            CASE
                WHEN transaction_status = 'Success'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate
FROM transactions
GROUP BY payment_method
ORDER BY success_rate DESC;

-- Failed transaction
SELECT
    payment_method,
    COUNT(*) AS failed_transactions,
    ROUND(SUM(amount), 2) AS failed_amount
FROM transactions
WHERE transaction_status = 'Failed'
GROUP BY payment_method
ORDER BY failed_transactions DESC;

-- Monthly payment trend
SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    COUNT(*) AS total_transactions,
    SUM(
        transaction_status = 'Success'
    ) AS successful_transactions,
    SUM(
        transaction_status = 'Failed'
    ) AS failed_transactions
FROM transactions
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month;

-- Top 10 Products
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
WHERE o.order_status = 'Completed'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;

-- Category performance
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS products,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
ORDER BY revenue DESC;

-- Customer spending rank
WITH customer_spending AS (
    SELECT
        u.user_id,
        u.name,
        SUM(o.total_amount) AS total_spent
    FROM users u
    JOIN orders o
        ON u.user_id = o.user_id
    WHERE o.order_status = 'Completed'
    GROUP BY u.user_id, u.name
)
SELECT
    user_id,
    name,
    ROUND(total_spent, 2) AS total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS spending_rank
FROM customer_spending
ORDER BY spending_rank;

-- Region wise customer ranking
WITH state_sales AS (
    SELECT
        u.state,
        SUM(o.total_amount) AS revenue
    FROM users u
    JOIN orders o
        ON u.user_id = o.user_id
    WHERE o.order_status = 'Completed'
    GROUP BY u.state
)
SELECT
    state,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM state_sales
ORDER BY revenue_rank;