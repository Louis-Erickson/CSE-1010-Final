
def calc_balance(income, expenses):
    account_balance = income - sum(expenses)
    print(f"\nGreat, your balance is: ${account_balance:.2f}")
    return account_balance

def financial_status(balance):
    if balance > 0:
        status = "Great! You are saving money!"
    elif balance == 0:
        status = "You are breaking even."
    else:
        status = "WARNING: You are overspending!"
    print(status)
    return status


