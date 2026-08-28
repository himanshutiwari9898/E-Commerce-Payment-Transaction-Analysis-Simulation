from database import get_connection


def transaction_history():

    print("\n==========================================")
    print("          TRANSACTION HISTORY")
    print("==========================================")

    try:
        user_id = int(input("Enter User ID: "))
    except ValueError:
        print("\nInvalid User ID!")
        return

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch user's transactions
    query = """
    SELECT
        transaction_id,
        order_id,
        transaction_date,
        payment_method,
        amount,
        transaction_status,
        transaction_reference
    FROM transactions
    WHERE user_id = %s
    ORDER BY transaction_date DESC, transaction_id DESC
    """

    cursor.execute(query, (user_id,))
    transactions = cursor.fetchall()

    if not transactions:
        print("\nNo transactions found for this user.")

        cursor.close()
        connection.close()
        return

    print("\n---------------- TRANSACTIONS ----------------")

    for transaction in transactions:

        print(
            f"\nTransaction ID : {transaction['transaction_id']}"
        )
        print(
            f"Order ID       : {transaction['order_id']}"
        )
        print(
            f"Date           : {transaction['transaction_date']}"
        )
        print(
            f"Payment Method : {transaction['payment_method']}"
        )
        print(
            f"Amount         : ₹{float(transaction['amount']):,.2f}"
        )
        print(
            f"Status         : {transaction['transaction_status']}"
        )
        print(
            f"Reference      : {transaction['transaction_reference']}"
        )
        print("--------------------------------------------")

    # Summary
    total_transactions = len(transactions)

    successful = sum(
        1
        for t in transactions
        if t["transaction_status"] == "Success"
        )
    failed = sum(
        1
        for t in transactions
        if t["transaction_status"] == "Failed"
        )
    pending = sum(
        1
        for t in transactions
        if t["transaction_status"] == "Pending"
        )
    refunded = sum(
        1
        for t in transactions
        if t["transaction_status"] == "Refunded"
        )
    total_amount = sum(
        float(t["amount"])
        for t in transactions
        if t["transaction_status"] == "Success"
    )

    print("\n==========================================")
    print("             PAYMENT SUMMARY")
    print("==========================================")

    print("Total Transactions :", total_transactions)
    print("Successful         :", successful)
    print("Failed             :", failed)
    print("Successful Amount  :", f"₹{total_amount:,.2f}")

    if total_transactions > 0:

        success_rate = (
            successful / total_transactions
        ) * 100

        print(
            "Success Rate       :",
            f"{success_rate:.2f}%"
        )

    cursor.close()
    connection.close()