from decimal import Decimal, ROUND_HALF_UP

def format_amount(amount):
    decimal_amount = Decimal(str(amount))
    precision = "0.01"
    rounded_amount = decimal_amount.quantize(Decimal(precision), rounding=ROUND_HALF_UP)
    return rounded_amount


def compute_expenses(expenses):
    total = 0
    for expense in expenses:
        total += expense.amount
    return total


def get_balances(expenses, group_aliases):
    balances = {}
    for alias in group_aliases:
        balances[alias] = 0

    for expense in expenses:
        payer = expense.payer.alias
        splitters = expense.splitters.all()
        amount = expense.amount
        split_amount = amount / len(splitters)
        split_amount = format_amount(split_amount)
        for splitter in splitters:
            is_payer = splitter.alias == payer
            current_balance = balances[splitter.alias]
            expense_balance = amount - split_amount if is_payer else split_amount
            balance = current_balance + expense_balance if is_payer else current_balance - expense_balance
            balances[splitter.alias] = balance

    return balances

