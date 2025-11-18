from library.classes_10 import Budget
from library import functions

def update_expenses(income):
    """
    Add extra expenses to existing categories, save them, and display totals and balance.
    """
    print("Update your existing expenses!\n")
    
    categories = ["Grocery", "Car"]
    
    existing_budgets = {}
    try:
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        current_category = None
        for line in lines:
            line = line.strip()
            if line in categories:
                current_category = line
                if current_category not in existing_budgets:
                    existing_budgets[current_category] = {}
            elif line != "" and current_category:
                parts = line.split(": $")
                if len(parts) == 2:
                    name = parts[0].strip()
                    cost = float(parts[1].strip())
                    existing_budgets[current_category][name] = cost
    except FileNotFoundError:
        for cat in categories:
            existing_budgets[cat] = {}

    for category_name in categories:
        choice = input(f"Do you want to add expenses for {category_name}? (y/n): ").strip().lower()
        if choice == "y":
            budget = Budget(category_name)
            budget.expenses = existing_budgets.get(category_name, {})
            budget.add_expenses()
            existing_budgets[category_name] = budget.expenses

    save_choice = input("Do you want to save these updates to file? (y/n): ").strip().lower()
    if save_choice == "y":
        with open("expenses.txt", "w") as file:
            for category in categories:
                file.write(f"{category}\n")
                for name, cost in existing_budgets[category].items():
                    file.write(f"{name} : ${cost:.2f}\n")
                file.write("\n")
        print("Updates saved successfully!\n")
    else:
        print("Updates discarded.\n")

    total_expenses = []
    for category_name in categories:
        budget = Budget(category_name)
        budget.expenses = existing_budgets.get(category_name, {})
        total_expenses.append(budget.get_expenses())
        budget.get_expenses_list()
    
    balance = functions.calc_balance(income, total_expenses)
    functions.financial_status(balance)