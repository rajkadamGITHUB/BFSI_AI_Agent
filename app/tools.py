def get_account_balance():
    return {
        "account": "XXXX1234",
        "balance": 52450,
        "currency": "INR"
    }


def get_recent_transactions():

    return {
        "account": "XXXX1234",
        "transactions": [
            {
                "date": "2026-10-05",
                "description": "UPI Payment",
                "amount": -500
            },
            {
                "date": "2026-10-04",
                "description": "Salary Credit",
                "amount": 45000
            },
            {
                "date": "2026-10-03",
                "description": "ATM Withdrawal",
                "amount": -2000
            }
        ]
    }


def get_card_status():

    return {
        "card": "XXXX5678",
        "status": "Active"
    }