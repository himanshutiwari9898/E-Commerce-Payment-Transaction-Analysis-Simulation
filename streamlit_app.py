import streamlit as st
import pandas as pd
from database import get_connection
import random
from datetime import datetime


st.set_page_config(
    page_title="E-Commerce Payment Gateway",
    page_icon="💳",
    layout="wide"
)


st.title("💳 E-Commerce Payment Transaction Analysis & Simulation")
st.caption("Python + MySQL + SQL Analytics")


# --------------------------------------------------
# DATABASE FUNCTIONS
# --------------------------------------------------

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


def insert_transaction(
    transaction_id,
    order_id,
    user_id,
    payment_method,
    amount,
    status,
    reference
):

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
        status,
        reference
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_user_transactions(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

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
    ORDER BY transaction_date DESC,
             transaction_id DESC
    """

    cursor.execute(query, (user_id,))
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Payment Simulation",
        "Transaction History"
    ]
)


# --------------------------------------------------
# PAYMENT SIMULATION
# --------------------------------------------------

if page == "Payment Simulation":

    st.header("Payment Simulation")

    order_id = st.number_input(
        "Enter Order ID",
        min_value=1,
        step=1
    )

    if st.button("Fetch Order"):

        order = get_order_details(order_id)

        if order is None:

            st.error("Order not found.")

        elif order["order_status"] != "Completed":

            st.warning(
                f"Payment cannot be processed. "
                f"Order status: {order['order_status']}"
            )

        else:

            st.session_state["order"] = order

    if "order" in st.session_state:

        order = st.session_state["order"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Order ID",
            order["order_id"]
        )

        col2.metric(
            "User ID",
            order["user_id"]
        )

        col3.metric(
            "Amount",
            f"₹{float(order['total_amount']):,.2f}"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking",
                "Wallet"
            ]
        )

        if st.button("Process Payment"):

            status = random.choices(
                ["Success", "Failed"],
                weights=[85, 15]
            )[0]

            transaction_id = generate_transaction_id()

            reference = f"TXN{transaction_id}"

            insert_transaction(
                transaction_id,
                order["order_id"],
                order["user_id"],
                payment_method,
                float(order["total_amount"]),
                status,
                reference
            )

            if status == "Success":

                st.success(
                    f"Payment Successful! "
                    f"Transaction: {reference}"
                )

            else:

                st.error(
                    f"Payment Failed. "
                    f"Transaction: {reference}"
                )

            st.info(
                f"Amount: ₹{float(order['total_amount']):,.2f}"
            )


# --------------------------------------------------
# TRANSACTION HISTORY
# --------------------------------------------------

elif page == "Transaction History":

    st.header("Transaction History")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    if st.button("View Transactions"):

        transactions = get_user_transactions(user_id)

        if not transactions:

            st.warning(
                "No transactions found."
            )

        else:

            df = pd.DataFrame(transactions)

            st.dataframe(
                df,
                use_container_width=True
            )

            successful = sum(
                df["transaction_status"] == "Success"
            )

            failed = sum(
                df["transaction_status"] == "Failed"
            )

            pending = sum(
                df["transaction_status"] == "Pending"
            )

            refunded = sum(
                df["transaction_status"] == "Refunded"
            )

            successful_amount = df.loc[
                df["transaction_status"] == "Success",
                "amount"
            ].sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Transactions",
                len(df)
            )

            col2.metric(
                "Successful",
                successful
            )

            col3.metric(
                "Failed",
                failed
            )

            col4.metric(
                "Successful Amount",
                f"₹{float(successful_amount):,.2f}"
            )