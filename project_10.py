import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"

import customtkinter as ctk
from tkinter import messagebox, simpledialog
from library.classes_10 import Budget
from library.add_expenses import update_expenses
from library import functions

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BudgetBuddy – GUI")
        self.geometry("650x600")
        self.resizable(False, False)

        # Data
        self.income = 0
        self.budgets = {}

        # --- Header ---
        ctk.CTkLabel(self, text="Welcome to BudgetBuddy!", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # --- Income input ---
        frame_income = ctk.CTkFrame(self)
        frame_income.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(frame_income, text="Enter your income:").pack(side="left", padx=5)
        self.entry_income = ctk.CTkEntry(frame_income)
        self.entry_income.pack(side="left", padx=5)
        ctk.CTkButton(frame_income, text="Set Income", command=self.set_income).pack(side="left", padx=5)

        # --- Action Buttons ---
        frame_buttons = ctk.CTkFrame(self)
        frame_buttons.pack(pady=10, padx=20, fill="x")
        self.btn_add_expenses = ctk.CTkButton(frame_buttons, text="Add Expenses", command=self.add_expenses, state="disabled")
        self.btn_add_expenses.pack(side="left", padx=10)
        self.btn_update_expenses = ctk.CTkButton(frame_buttons, text="Update Expenses", command=self.update_expenses_gui, state="disabled")
        self.btn_update_expenses.pack(side="left", padx=10)
        self.btn_reset = ctk.CTkButton(frame_buttons, text="Reset All Expenses", command=self.reset_expenses)
        self.btn_reset.pack(side="left", padx=10)

        # --- Output text box ---
        self.text_output = ctk.CTkTextbox(self, width=600, height=400)
        self.text_output.pack(pady=10, padx=20)
        self.text_output.insert("0.0", "Enter your income to begin...\n")

    # --- Methods ---
    def set_income(self):
        try:
            self.income = float(self.entry_income.get())
            messagebox.showinfo("Income Set", f"Income set to ${self.income:.2f}")
            self.entry_income.configure(state="disabled")
            self.btn_add_expenses.configure(state="normal")
            self.btn_update_expenses.configure(state="normal")
            self.show_totals()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for income.")

    def add_expenses(self):
        for category in ["Grocery", "Car"]:
            if category not in self.budgets:
                self.budgets[category] = Budget(category)
            # GUI-based inputs
            while True:
                add_more = messagebox.askyesno("Add Expense", f"Do you want to add an expense for {category}?")
                if not add_more:
                    break
                name = simpledialog.askstring("Expense Name", f"Enter expense name for {category}:", parent=self)
                if not name:
                    continue
                cost = simpledialog.askfloat("Expense Amount", f"Enter amount for {name}:", parent=self)
                if cost is None:
                    continue
                self.budgets[category].expenses[name] = cost
        self.show_totals()

    def update_expenses_gui(self):
        if self.income == 0:
            messagebox.showerror("Error", "Please enter your income first!")
            return
        update_expenses(self.income)
        messagebox.showinfo("Update Complete", "Expenses updated successfully!")
        self.show_totals()

    def show_totals(self):
        self.text_output.delete("0.0", "end")
        total_expenses = []

        for category, budget in self.budgets.items():
            total = budget.get_expenses()
            total_expenses.append(total)
            self.text_output.insert("end", f"{category} Expenses Total: ${total:.2f}\n")
            for name, cost in budget.expenses.items():
                self.text_output.insert("end", f"  {name}: ${cost:.2f}\n")
            self.text_output.insert("end", "\n")

        # Balance and status using functions.py
        balance = functions.calc_balance(self.income, total_expenses)
        status = functions.financial_status(balance)  # make sure this returns a string
        self.text_output.insert("end", f"Account Balance: ${balance:.2f}\nStatus: {status}\n")

    def reset_expenses(self):
        self.budgets = {}
        with open("expenses.txt", "w") as f:
            pass
        self.text_output.delete("0.0", "end")
        self.text_output.insert("0.0", "All expenses have been reset.\n")
        messagebox.showinfo("Reset", "All expenses reset.")


# --- Run GUI ---
if __name__ == "__main__":
    print("Launching GUI...")
    app = BudgetBuddyApp()
    app.mainloop()