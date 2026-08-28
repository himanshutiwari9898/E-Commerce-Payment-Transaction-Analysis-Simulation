from database import get_connection
import random
from datetime import datetime


def generate_transaction_id():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT MAX(transaction_id) FROM transactions"
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result[0] is None:
        return 50001

    return result[0] + 1


def get_order_details(order_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        order_id,
        user_id,
        total_amount,
        order_status
    FROM orders
    WHERE order_id = %s
    """

    cursor.execute(query, (order_id,))
    order = cursor.fetchone()

    cursor.close()
    connection.close()

    return order


def simulate_payment():

    print("\n==========================================")
    print("       SECURE PAYMENT GATEWAY")
    print("          PAYMENT SIMULATION")
    print("==========================================")

    try:
        order_id = int(input("\nEnter Order ID: "))

    except ValueError:
        print("\nInvalid Order ID!")
        return

    # Get order details from MySQL
    order = get_order_details(order_id)

    if order is None:
        print("\nOrder not found!")
        return

    # Only completed orders can be paid
    if order["order_status"] != "Completed":

        print("\nPayment cannot be processed.")
        print("Current Order Status:", order["order_status"])

        return

    user_id = order["user_id"]
    amount = float(order["total_amount"])

    print("\n---------- ORDER DETAILS ----------")
    print("Order ID :", order_id)
    print("User ID  :", user_id)
    print("Amount   :", f"₹{amount:,.2f}")

    # Payment methods
    print("\nSelect Payment Method")
    print("1. UPI")
    print("2. Credit Card")
    print("3. Debit Card")
    print("4. Net Banking")
    print("5. Wallet")

    choice = input("\nEnter choice: ")

    payment_methods = {
        "1": "UPI",
        "2": "Credit Card",
        "3": "Debit Card",
        "4": "Net Banking",
        "5": "Wallet"
    }

    if choice not in payment_methods:

        print("\nInvalid payment method!")
        return

    payment_method = payment_methods[choice]

    # Simulate payment result
    transaction_status = random.choices(
        ["Success", "Failed"],
        weights=[85, 15]
    )[0]

    # Generate transaction ID
    transaction_id = generate_transaction_id()

    transaction_reference = f"TXN{transaction_id}"

    # Insert transaction into database
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO transactions
    (
        transaction_id,
        order_id,
        user_id,
        transaction_date,
        payment_method,
        amount,
        transaction_status,
        transaction_reference
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        transaction_id,
        order_id,
        user_id,
        datetime.now().date(),
        payment_method,
        amount,
        transaction_status,
        transaction_reference
    )

    cursor.execute(query, values)

    connection.commit()

    print("\n==========================================")
    print("          PAYMENT RESULT")
    print("==========================================")

    print("Transaction ID :", transaction_id)
    print("Reference      :", transaction_reference)
    print("Order ID       :", order_id)
    print("Payment Method :", payment_method)
    print("Amount         :", f"₹{amount:,.2f}")
    print("Status         :", transaction_status)

    cursor.close()
    connection.close()