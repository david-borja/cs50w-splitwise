# Final Project | Splitwise Clone

## Overview
The Splitwise Clone is a web-based application designed to simplify shared expenses. It allows users to manage group expenses, track balances, and manage reimbursements efficiently. Unlike a social network or e-commerce site, this project focuses specifically on collaborative expense management.

## Distinctiveness and Complexity
This project is distinct from other course projects in both purpose and implementation:
- **Not a Social Network**: The project does not include user feeds, posts, or friend lists. Its primary focus is on financial transactions and group expenses management.
- **Not E-Commerce**: While the application deals with financial information, it does not involve product catalogs, shopping carts. In the same way, it doesn't include anything related to auctions or bids.

### Key Features
- **Group Expense Management**: Users can create groups, add members and start adding expenses.
- **Expense Creation**: Users can submit expenses detailing the payer, amount and splitters of the expense.
- **Detailed Transaction History**: Users can view a complete log of expenses and settlements.
- **Balance Tracking**: Displays a clear breakdown of amounts owed or owed to others.
- **Suggested Reimbursements Functionality**: Allows users to see the calculated reimbursements needed to settle the group finances. In addition, it provides an easy way to mark debts as paid and update balances accordingly.
- **Responsive Design**: Built with a mobile-first approach using Django Tailwind for styling.

The project demonstrates complexity through:
- Custom backend logic for calculating balances and suggested reimbursements from expenses.
  - Balances are always dynamic and calculated on the fly, while expenses are permanent and stored in the db.
  - Settled reimbursements are seen on the expenses feed, but their amount is not taken in account for the calculated 'total expenses' and 'my expenses'
- Separate User and Alias model - created group memebers are regarded as universally unique aliases.
  - Future feature: group members can receive a link to claim their alias in a group and become app users
- Custom interactivity of the app state with JavaScript combined with modifying the url accordingly (ie: expenses/balances section).
- Integration of Django Tailwind for enhanced styling and responsiveness.
- Mock data and seed script to easily see the app functionality in action.

## File Structure
The main files that power up the app are found in:
- /templates: all the html pages and reusable UI components
- /templatetags/custom_tags.py: where tags are defined in order to use UI components, filters and svg utilities
- utils.py: calculation functionality, extracted to allow reusability or to simplify views.py
- views.py: this file manages the server funcionality depending on the endpoint. Here we can find the functions to list, create, check, validate, and update resources in the db

Inline JavaScript code is found in the very same html files, using the script tag, and the modern type module. This allows us to load JavaScript after HTML without listening to the DOMContentLoaded event.
The JS code is found in:
- group.html
- create-expense.html
- create-group.html

## Installation (one time):
### Option 1 (granular deps)
- python3 manage.py migrate
- python3 manage.py seed_db
- python3 -m pip install django-tailwind
- python3 -m pip install 'django-tailwind[reload]'
- python3 manage.py tailwind install

### Option 2 (deps with requirements.txt)
- python3 manage.py migrate
- python3 manage.py seed_db
- pip3 install -r requirements.txt
- python3 manage.py tailwind install

## Project Start (every time to get the project running):
- python3 manage.py tailwind start
- python3 manage.py runserver

Default app credentials (recommended for validations):
- user: david
- password: 1234