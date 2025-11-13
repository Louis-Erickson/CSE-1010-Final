class Budget:
    def __init__(self, category):
        """
        Initializes a budget category.
        :param category: String name of the category, e.g., "Grocery" or "Car"
        """
        self.category = category
        self.expenses = {}  # Dictionary to store expenses: {name: cost}

    def add_expenses(self):
        """
        Add new expenses interactively to this category.
        """
        try:
            num = int(input(f"How many expenses for {self.category}? "))
        except ValueError:
            print("Invalid input. Setting number of expenses to 0.")
            num = 0

        for i in range(num):
            expense_name = input(f"Enter type of expense #{i + 1}: ")
            while True:
                try:
                    expense_cost = float(input(f"Enter amount for {expense_name}: $"))
                    break
                except ValueError:
                    print("Invalid amount. Please enter a number.")

            # Add or update expense in dictionary
            self.expenses[expense_name] = expense_cost

        # Write changes to file immediately (optional, can skip if using addexpenses.py)
        self.write_to_file()

    def write_to_file(self):
        """
        Writes this category and its expenses to 'expenses.txt'.
        Appends by default.
        """
        with open("expenses.txt", "a") as file:
            file.write(f"{self.category}\n")
            for name, cost in self.expenses.items():
                file.write(f"{name} : ${cost:.2f}\n")
            file.write("\n")

    def get_expenses(self):
        """
        Returns total of this category and prints it.
        """
        total = sum(self.expenses.values())
        print(f"Total {self.category} expenses: ${total:.2f}")
        return total

    def get_expenses_list(self):
        """
        Prints all individual expenses for this category.
        """
        if not self.expenses:
            print(f"\nNo expenses recorded for {self.category}.")
            return

        print(f"\nList of {self.category} expenses:")
        for name, cost in self.expenses.items():
            print(f"{name} : ${cost:.2f}")