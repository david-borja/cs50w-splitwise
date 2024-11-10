# Expense Sharing App Requirements (Splitwise Clone)

## 1. Group Creation
- Users should be able to create a new group for a specific event or activity (e.g., a trip, a dinner, etc.).
- When creating a group, the user can specify a group name and add a brief description.
- The group creator can invite other users to join by sharing a unique link or code.

## 2. Participant Management
- Users should be able to add and remove participants in a group.
- Each participant should have a name and an optional avatar for identification.
- Participants may not need a registered account to join, but if they are unregistered, they should appear as "guests" with customizable names.

## 3. Adding Expenses
- Users should be able to add an expense to the group. Each expense entry should include:
  - The name or description of the expense (e.g., “Dinner at restaurant”).
  - The total amount.
  - The date the expense occurred.
  - The person who paid for the expense.
  - **Optional**: a photo or note to give more context to the expense.
- Users can specify how to split the expense among participants (e.g., equally, by specific percentages, or by custom amounts).

## 4. Expense Splitting and Balances
- The app should automatically calculate each user’s balance based on the added expenses and the specified division for each expense.
- Each user should be able to view a personal summary of their balance: how much they’ve paid, how much they owe, and how much others owe them.
- The interface should display an overall balance summary for the group, highlighting debts between participants in a simplified format.

## 5. Transaction and Balance Summary
- Users should have access to a transaction history for the group, displaying all added expenses with details (who paid, the amount, and the split breakdown).
- To facilitate payment, the app should simplify the total transactions into a summary showing who owes whom and how much.

## 6. Notifications and Updates
- Whenever a new expense is added or the balance changes, all participants should receive a notification to stay updated.
- **Optional**: the app can send reminders to users to settle their outstanding balances.

## 7. Optional Payment Integration
- The app could include optional functionality for users to make payments directly within the app, using external payment services like PayPal or Venmo.
- This feature should only be available if both parties agree to settle debts through this method.

## 8. Data Export
- Users should have the option to export their group’s balance summary and transaction history in a PDF or CSV format for external record-keeping.

## 9. Privacy and Security Settings
- Each group should have privacy settings to control who can join or view the group details.
- Only group participants should have access to the group's information, with options to remove or block users if needed.

## 10. User Interface (UI)
- The app should feature a friendly, easy-to-navigate interface, ideally with a main dashboard that displays active groups and each group's overall balance.
- Each group should have its own section where participants can view all expense and balance details.
- The app MUST be mobile-responsive
