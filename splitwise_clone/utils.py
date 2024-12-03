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


def get_top_debtors(balances):
    debtors = []
    sorted_balances = sort_balances(balances)
    for balance in sorted_balances:
        person = list(balance.keys())[0]
        balance_amount = balance[person]
        if balance_amount < 0:
            debtors.append(balance)
        else:
            return debtors


def get_top_lenders(balances):
    lenders = []
    sorted_balances = sort_balances(balances, "DSC")
    for balance in sorted_balances:
        person = list(balance.keys())[0]
        balance_amount = balance[person]
        if balance_amount > 0:
            lenders.append(balance)
        else:
            return lenders


def get_suggested_reimbursements(balances):
    top_debtors = get_top_debtors(balances)
    top_lenders = get_top_lenders(balances)

    reimbursements = {}
    for debtor in top_debtors:
        debtor_name = list(debtor.keys())[0]
        indebted_amount = debtor[debtor_name]

        for index, lender in enumerate(top_lenders):
            lender_name = list(lender.keys())[0]
            lended_amount = lender[lender_name]
            if lended_amount > 0 and abs(indebted_amount) > 0:
                reimbursement_amount = (
                    abs(indebted_amount)
                    if (abs(indebted_amount) <= lended_amount)
                    else lended_amount
                )
                if debtor_name not in reimbursements:
                    reimbursements[debtor_name] = {}

                reimbursements[debtor_name][lender_name] = reimbursement_amount
                lended_amount = lended_amount - reimbursement_amount
                balances[lender_name] = lended_amount
                top_lenders[index][lender_name] = lended_amount
                indebted_amount = abs(indebted_amount) - reimbursement_amount
                balances[debtor_name] = indebted_amount

    return reimbursements


def flatten_reimbursements(reimbursements):
    flat_reimbursements = []
    for key, value in reimbursements.items():
        sender = key
        receivers_obj = value
        for receiver_key, amount_value in receivers_obj.items():
            flat_reimbursements.append(
                {"sender": sender, "receiver": receiver_key, "amount": amount_value}
            )

    return flat_reimbursements


def sort_balances(balances, sort="ASC"):
    reverse = True if sort == "DSC" else False
    balances_tuple_pairs = balances.items()
    sorted_data = [
        {key: value}
        for key, value in sorted(
            balances_tuple_pairs, key=lambda item: item[1], reverse=reverse
        )
    ]

    return sorted_data


def filter_reimbursements_by_person(reimbursements, person):
    return list(
        filter(
            lambda r: r["sender"] == person or r["receiver"] == person, reimbursements
        )
    )


def filter_reimbursements_exclude_person(reimbursements, person):
    return list(
        filter(
            lambda r: r["sender"] != person and r["receiver"] != person, reimbursements
        )
    )
