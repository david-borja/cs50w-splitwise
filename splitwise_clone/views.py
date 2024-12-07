from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.urls import reverse
from .utils import (
    compute_expenses,
    get_balances,
    get_suggested_reimbursements,
    flatten_reimbursements,
    filter_reimbursements_by_person,
    filter_reimbursements_exclude_person,
    decimals,
)
from .models import User, UserGroup, UserAlias, Expense

EXPENSES_SECTION = "expenses"
BALANCES_SECTION = "balances"
DEFAULT_SECTION = EXPENSES_SECTION

@login_required()
def index(request):
    groups = UserGroup.objects.all()
    create_group_form_url = reverse('create_group')
    return render(request, "splitwise_clone/index.html", {
        "groups": groups,
        "create_group_form_url": create_group_form_url,
    })


@login_required()
def create_group(request):
    if request.method == "POST":
        participants = []
        group_name = request.POST.get("group_name")
        participantIterator = 0
        participant = request.POST.get(f"participant-{participantIterator + 1}", None)
        while participant:
            participants.append(participant)
            participantIterator = participantIterator + 1
            participant = request.POST.get(f"participant-{participantIterator + 1}", None)

        group = UserGroup(name=group_name)
        group.save()
        created_group = UserGroup.objects.get(name=group_name)
        me_as_participant = participants[0]
        UserAlias.objects.create(user=request.user, alias=me_as_participant, group=created_group)

        rest_of_participants = participants[1:]
        user_aliases = []
        for participant in rest_of_participants:
            user_aliases.append(UserAlias(alias=participant, group=created_group))
        UserAlias.objects.bulk_create(user_aliases)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "splitwise_clone/create-group.html")


@login_required()
def create_expense(request):
    if request.method == "POST":
        group_id = request.POST["group_id"]
        group = UserGroup.objects.get(pk=group_id)
        data = request.POST.dict()
        amount = decimals(float(data["amount"]))
        splitter_alias_ids = []
        for key, value in data.items():
            if value == "on":
                splitter_alias_ids.append(key)

        splitters = UserAlias.objects.filter(pk__in=splitter_alias_ids)
        expense = Expense(
            name=data["name"],
            group=group,
            amount=amount,
            payer=UserAlias.objects.get(pk=data["payer"]),
        )

        with transaction.atomic():
            expense.splitters.set(splitters)
            expense.save()

        return HttpResponseRedirect(reverse(
            "group_section",
            kwargs={"group_id": group_id, "section": data["redirect_section"] }))

    group_id = request.GET.get('group_id')
    participants = UserAlias.objects.filter(group=group_id).order_by('alias')

    current_user_as_participant = None
    for participant in participants:
        participant.is_current_user = participant.user == request.user
        if participant.is_current_user:
            current_user_as_participant = participant

    return render(request, "splitwise_clone/create-expense.html", {
        "group_id": group_id,
        "participants": participants,
        "current_user_as_participant": current_user_as_participant,
})

@login_required()
def group(request, group_id, section=DEFAULT_SECTION):
    if section not in [EXPENSES_SECTION, BALANCES_SECTION]:
        return HttpResponse("Invalid section", status=404)

    group = UserGroup.objects.get(pk=group_id)
    participants = UserAlias.objects.filter(group=group_id).order_by('alias')

    group_aliases = []
    for participant in participants:
        participant.initial_letter = participant.alias[0].upper()
        participant.is_current_user = participant.user == request.user
        group_aliases.append(participant.alias)

    expenses = group.group_expenses.order_by('-timestamp')
    total_expenses_amount = compute_expenses(expenses)

    my_expenses = UserAlias.objects.get(user=request.user, group=group).acquisitions.all()
    my_expenses_amount = compute_expenses(my_expenses)

    balances = get_balances(expenses, group_aliases)
    balance_summary_amount = 0
    current_user_alias = ''
    for participant in participants:
        participant.balance = balances[participant.alias]
        if participant.is_current_user:
            balance_summary_amount = participant.balance
            current_user_alias = participant.alias

    suggested_reimbursements = get_suggested_reimbursements(balances)
    flat_reimbursements = flatten_reimbursements(suggested_reimbursements)

    for reimbursement in flat_reimbursements:
        reimbursement["sender_id"] = UserAlias.objects.get(
            alias=reimbursement["sender"],
            group=group
        ).id
        reimbursement["receiver_id"] = UserAlias.objects.get(
            alias=reimbursement["receiver"],
            group=group
        ).id

    my_reimbursements = filter_reimbursements_by_person(
        flat_reimbursements, current_user_alias
    )
    other_reimbursements = filter_reimbursements_exclude_person(
        flat_reimbursements, current_user_alias
    )

    return render(
        request,
        "splitwise_clone/group.html",
        {
            "group": group,
            "section": section,
            "expenses_visibility": "block" if section == EXPENSES_SECTION else "hidden",
            "balances_visibility": "block" if section == BALANCES_SECTION else "hidden",
            "SECTIONS": {
                "EXPENSES": EXPENSES_SECTION,
                "BALANCES": BALANCES_SECTION,
            },
            "participants": participants,
            "current_user_alias": current_user_alias,
            "expenses": expenses,
            "expenses_summary": {
                "my_expenses": my_expenses_amount,
                "total_expenses": total_expenses_amount,
            },
            "balance_summary": {"amount": balance_summary_amount},
            "my_reimbursements": my_reimbursements,
            "suggested_reimbursements": other_reimbursements,
            "create_expense_form_url": f"{reverse('create_expense')}?group_id={group_id}",
        },
    )

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "splitwise_clone/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "splitwise_clone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "splitwise_clone/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "splitwise_clone/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "splitwise_clone/register.html")
