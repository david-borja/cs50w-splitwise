from django.core.management.base import BaseCommand
from splitwise_clone.models import User, UserGroup, UserAlias
import json
import os


def json_reader(file_path):
    # Read JSON data from file
    with open(file_path, "r") as stream:
        data = json.load(stream)
    return data


def insert_groups(self, data):
    try:
        for item in data:
            name = item["name"]
            description = item["description"]
            icon = item["icon"]
            group = UserGroup(
                name=name,
                description=description,
                icon=icon,
            )
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Created group: '{name}'"))
        self.stdout.write(self.style.SUCCESS("GROUPS seeding completed."))
    except Exception as err:
        self.stdout.write(self.style.ERROR("An error occurred:", err))


def insert_users(self, data):
    try:
        for item in data:
            kwargs = {
                "username": item["username"],
                "email": item["email"],
                "password": item["password"],
                "is_superuser": item.get(
                    "is_superuser", False
                ),  # second argument is the fallback value
            }
            if kwargs["is_superuser"]:
                User.objects.create_superuser(**kwargs)
                self.stdout.write(
                    self.style.SUCCESS(f"Created superuser: '{item['username']}'")
                )
            else:
                User.objects.create_user(**kwargs)
                self.stdout.write(
                    self.style.SUCCESS(f"Created user '{item['username']}'")
                )
        self.stdout.write(self.style.SUCCESS("USERS seeding completed."))
    except Exception as err:
        self.stdout.write(self.style.ERROR("An error occurred:", err))


def insert_aliases(self, data):
    try:
        USERNAME = 'david'
        user = User.objects.get_by_natural_key(USERNAME)
        group_names = list(data.keys())
        for group_name in group_names:
            group = UserGroup.objects.get(name=group_name)
            participants = data[group_name]
            me_as_participant = participants[0]
            UserAlias.objects.create(user=user, alias=me_as_participant, group=group)
            self.stdout.write(
                self.style.SUCCESS(f"Created alias '{me_as_participant}'")
            )

            rest_of_participants = participants[1:]
            for participant in rest_of_participants:
                UserAlias.objects.create(alias=participant, group=group)
                self.stdout.write(
                    self.style.SUCCESS(f"Created alias '{participant}'")
                )
        self.stdout.write(self.style.SUCCESS("ALIAS seeding completed."))
    except Exception as err:
        self.stdout.write(self.style.ERROR("An error occurred:", err))


integrator_switch = {
    "users.json": insert_users,
    "groups.json": insert_groups,
    "aliases.json": insert_aliases,
}


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the JSON file
        seed_data_dir = os.path.join(script_dir, "../seed_data")
        data_file_names = ["users.json", "groups.json", "aliases.json"] # os.listdir(seed_data_dir)
        for data_file_name in data_file_names:
            if data_file_name not in integrator_switch:
                raise Exception(f"{data_file_name} file doesn't belong to seed data")
            integrator_func = integrator_switch[data_file_name]
            if not callable(integrator_func):
                raise Exception(
                    f"Integrator function for {data_file_name} is not callable"
                )
            json_file_path = os.path.join(seed_data_dir, f"{data_file_name}")
            data = json_reader(json_file_path)
            # Process and insert data into the database
            integrator_func(self, data)

        self.stdout.write(self.style.SUCCESS("DATABASE seeding completed."))
