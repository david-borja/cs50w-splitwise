import json
import os
import pytest
from django.contrib.auth.hashers import make_password
from splitwise_clone.models import User, UserGroup, UserAlias, Expense

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

SEED_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "management", "seed_data"
)


def _load_json(name):
    with open(os.path.join(SEED_DIR, name)) as f:
        return json.load(f)

@pytest.fixture(autouse=True)
def plain_static_storage(settings):
    settings.STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

@pytest.fixture(scope="session")
def seed_data():
    users = _load_json("users.json")
    groups = _load_json("groups.json")
    aliases = _load_json("aliases.json")
    expenses = _load_json("expenses.json")
    return users, groups, aliases, expenses


@pytest.fixture
def db_users(seed_data, db):
    users_data, _, _, _ = seed_data
    created = {}
    for u in users_data:
        user = User.objects.create_user(
            username=u["username"],
            email=u["email"],
            password=u["password"],
        )
        created[u["username"]] = user
    return created


@pytest.fixture
def db_groups(seed_data, db):
    _, groups_data, _, _ = seed_data
    created = {}
    for g in groups_data:
        group = UserGroup.objects.create(
            name=g["name"],
            description=g["description"],
            icon=g["icon"],
        )
        created[g["name"]] = group
    return created


@pytest.fixture
def db_aliases(seed_data, db_users, db_groups):
    _, _, aliases_data, _ = seed_data
    created_groups = {}
    for group_name, participant_list in aliases_data.items():
        group = db_groups[group_name]
        user = db_users["david"]
        alias_objects = []
        for i, alias_name in enumerate(participant_list):
            if i == 0:
                ua = UserAlias.objects.create(
                    alias=alias_name, group=group, user=user
                )
            else:
                ua = UserAlias.objects.create(alias=alias_name, group=group)
            alias_objects.append(ua)
        created_groups[group_name] = alias_objects
    return created_groups


@pytest.fixture
def db_expenses(seed_data, db_aliases):
    _, _, _, expenses_data = seed_data
    created = []
    for e in expenses_data:
        payer_alias = UserAlias.objects.get(alias=e["payer"])
        group = UserGroup.objects.get(name=e["group"])
        expense = Expense.objects.create(
            name=e["name"],
            amount=e["amount"],
            group=group,
            payer=payer_alias,
            icon=e["emoji"],
            timestamp=e["timestamp"],
        )
        splitters = []
        for splitter_name in e["splitters"]:
            splitters.append(UserAlias.objects.get(alias=splitter_name))
        expense.splitters.set(splitters)
        created.append(expense)
    return created


@pytest.fixture
def full_db(db_users, db_groups, db_aliases, db_expenses):
    return {
        "users": db_users,
        "groups": db_groups,
        "aliases": db_aliases,
        "expenses": db_expenses,
    }


@pytest.fixture
def live_server_url(live_server):
    return str(live_server)


@pytest.fixture
def authenticated_page(page, live_server_url, db_users):
    user = db_users["david"]
    page.goto(f"{live_server_url}/login")
    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', "1234")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{live_server_url}/")
    return page
