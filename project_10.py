import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from library.classes_10 import Budget
from library.add_expenses import update_expenses
from library import functions

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CustomInputDialog(ctk.CTkToplevel):
    """Custom large input dialog for expense entries"""
    def __init__(self, parent, title, prompt, input_type="string"):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x300")
        self.resizable(False, False)
        self.result = None
        self.input_type = input_type

        # Center the dialog
        self.transient(parent)
        self.grab_set()

        # Label
        label = ctk.CTkLabel(self, text=prompt, font=ctk.CTkFont(size=14), wraplength=450)
        label.pack(pady=20, padx=20)

        # Large input field
        self.input_field = ctk.CTkEntry(self, font=ctk.CTkFont(size=16), height=50, width=400)
        self.input_field.pack(pady=20, padx=20)
        self.input_field.focus()

        # Buttons frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ok_btn = ctk.CTkButton(button_frame, text="OK", command=self.ok_clicked, width=150, height=50, font=ctk.CTkFont(size=14))
        ok_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_clicked, width=150, height=50, font=ctk.CTkFont(size=14))
        cancel_btn.pack(side="left", padx=10)

        # Bind Enter key
        self.input_field.bind("<Return>", lambda e: self.ok_clicked())

    def ok_clicked(self):
        try:
            if self.input_type == "float":
                self.result = float(self.input_field.get())
            else:
                self.result = self.input_field.get()
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", f"Please enter a valid {self.input_type}")

    def cancel_clicked(self):
        self.result = None
        self.destroy()

    def get_result(self):
        self.wait_window()
        return self.result


class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BudgetBuddy – Budget Management System")
        self.geometry("1400x900")
        self.resizable(True, True)
        
        # Set minimum window size
        self.minsize(1000, 700)

        # Data
        self.income = 0
        self.budgets = {}

        # --- Main Container ---
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Header ---
        header_frame = ctk.CTkFrame(main_container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="💰 BudgetBuddy", font=ctk.CTkFont(size=32, weight="bold")).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Smart Budget Management System", font=ctk.CTkFont(size=14, weight="normal"), text_color="gray").pack(side="left", padx=10)

        # --- Income Section ---
        income_section = ctk.CTkFrame(main_container)
        income_section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(income_section, text="Income Setup", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        
        frame_income = ctk.CTkFrame(income_section, fg_color="transparent")
        frame_income.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_income, text="Monthly Income ($):", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.entry_income = ctk.CTkEntry(frame_income, font=ctk.CTkFont(size=12), width=200, height=40)
        self.entry_income.pack(side="left", padx=5)
        ctk.CTkButton(frame_income, text="Set Income", command=self.set_income, font=ctk.CTkFont(size=12), height=40).pack(side="left", padx=5)

        # --- Action Buttons Section ---
        button_section = ctk.CTkFrame(main_container)
        button_section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(button_section, text="Actions", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        
        frame_buttons = ctk.CTkFrame(button_section, fg_color="transparent")
        frame_buttons.pack(side="left", padx=10)
        
        self.btn_add_expenses = ctk.CTkButton(frame_buttons, text="➕ Add Expenses", command=self.add_expenses, state="disabled", font=ctk.CTkFont(size=12), height=40)
        self.btn_add_expenses.pack(side="left", padx=8)
        self.btn_load_expenses = ctk.CTkButton(frame_buttons, text="📂 Load Expenses", command=self.load_expenses_from_file, state="disabled", font=ctk.CTkFont(size=12), height=40)
        self.btn_load_expenses.pack(side="left", padx=8)
        self.btn_save_expenses = ctk.CTkButton(frame_buttons, text="💾 Save Expenses", command=self.save_expenses_to_file, state="disabled", font=ctk.CTkFont(size=12), height=40)
        self.btn_save_expenses.pack(side="left", padx=8)

        # --- Main Content Frame ---
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True)

        # --- Left Side: Summary & Expenses ---
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        ctk.CTkLabel(left_frame, text="📊 Expense Summary", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        summary_box = ctk.CTkFrame(left_frame, corner_radius=10)
        summary_box.pack(fill="both", expand=True)
        
        self.text_output = ctk.CTkTextbox(summary_box, font=ctk.CTkFont(size=11))
        self.text_output.pack(fill="both", expand=True, padx=15, pady=15)
        self.text_output.insert("0.0", "Enter your income to begin...\n")

        # --- Right Side: Pie Chart ---
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_frame, text="📈 Budget Breakdown", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        chart_box = ctk.CTkFrame(right_frame, corner_radius=10)
        chart_box.pack(fill="both", expand=True)
        
        self.chart_frame = ctk.CTkFrame(chart_box)
        self.chart_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # --- Methods ---
    def set_income(self):
        try:
            self.income = float(self.entry_income.get())
            messagebox.showinfo("Income Set", f"Income set to ${self.income:.2f}")
            self.entry_income.configure(state="disabled")
            self.btn_add_expenses.configure(state="normal")
            self.btn_load_expenses.configure(state="normal")
            self.btn_save_expenses.configure(state="normal")
            self.show_totals()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for income.")

    def add_expenses(self):
        for category in ["Grocery", "Car"]:
            if category not in self.budgets:
                self.budgets[category] = Budget(category)
            # GUI-based inputs
            while True:
                # Create custom dialog for yes/no
                dialog = ctk.CTkToplevel(self)
                dialog.title("Add Expense")
                dialog.geometry("450x200")
                dialog.resizable(False, False)
                dialog.transient(self)
                dialog.grab_set()

                add_more = False
                
                label = ctk.CTkLabel(dialog, text=f"Do you want to add an expense for {category}?", font=ctk.CTkFont(size=14))
                label.pack(pady=30)

                button_frame = ctk.CTkFrame(dialog)
                button_frame.pack(pady=20)

                def yes_clicked():
                    nonlocal add_more
                    add_more = True
                    dialog.destroy()

                def no_clicked():
                    nonlocal add_more
                    add_more = False
                    dialog.destroy()

                yes_btn = ctk.CTkButton(button_frame, text="Yes", command=yes_clicked, width=150, height=50, font=ctk.CTkFont(size=14))
                yes_btn.pack(side="left", padx=10)

                no_btn = ctk.CTkButton(button_frame, text="No", command=no_clicked, width=150, height=50, font=ctk.CTkFont(size=14))
                no_btn.pack(side="left", padx=10)

                dialog.wait_window()

                if not add_more:
                    break
                
                # Use custom large input dialog for name
                name_dialog = CustomInputDialog(self, "Expense Name", f"Enter expense name for {category}:", "string")
                name = name_dialog.get_result()
                if not name:
                    continue
                
                # Use custom large input dialog for cost
                cost_dialog = CustomInputDialog(self, "Expense Amount", f"Enter amount for {name}:", "float")
                cost = cost_dialog.get_result()
                if cost is None:
                    continue
                
                self.budgets[category].expenses[name] = cost
        self.show_totals()

    def save_expenses_to_file(self):
        """Save current expenses to expenses.txt file"""
        try:
            with open("expenses.txt", "w") as f:
                for category in ["Grocery", "Car"]:
                    if category in self.budgets:
                        f.write(f"{category}\n")
                        for name, cost in self.budgets[category].expenses.items():
                            f.write(f"{name} : ${cost:.2f}\n")
                        f.write("\n")
            messagebox.showinfo("Success", "Expenses saved to expenses.txt!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save expenses: {str(e)}")

    def load_expenses_from_file(self):
        """Load expenses from expenses.txt file"""
        try:
            if not os.path.exists("expenses.txt"):
                messagebox.showwarning("File Not Found", "expenses.txt does not exist yet.")
                return
            
            with open("expenses.txt", "r") as f:
                lines = f.readlines()
            
            current_category = None
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Check if it's a category (Grocery or Car)
                if line in ["Grocery", "Car"]:
                    current_category = line
                    if current_category not in self.budgets:
                        self.budgets[current_category] = Budget(current_category)
                elif current_category and " : $" in line:
                    # Parse expense line: "name : $amount"
                    try:
                        expense_name, amount_str = line.split(" : $")
                        amount = float(amount_str)
                        self.budgets[current_category].expenses[expense_name] = amount
                    except (ValueError, IndexError):
                        continue
            
            self.show_totals()
            messagebox.showinfo("Success", "Expenses loaded from expenses.txt!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {str(e)}")

    def show_totals(self):
        self.text_output.delete("0.0", "end")
        total_expenses = []
        category_totals = {}

        for category, budget in self.budgets.items():
            total = budget.get_expenses()
            total_expenses.append(total)
            category_totals[category] = total
            self.text_output.insert("end", f"{category} Expenses Total: ${total:.2f}\n")
            for name, cost in budget.expenses.items():
                self.text_output.insert("end", f"  {name}: ${cost:.2f}\n")
            self.text_output.insert("end", "\n")

        # Balance and status using functions.py
        balance = functions.calc_balance(self.income, total_expenses)
        status = functions.financial_status(balance)  # make sure this returns a string
        self.text_output.insert("end", f"Account Balance: ${balance:.2f}\nStatus: {status}\n")

        # Update pie chart
        self.update_pie_chart(category_totals, balance)

    def update_pie_chart(self, category_totals, balance):
        """Update the pie chart to show expense breakdown with leftover income"""
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not category_totals and balance <= 0:
            # Show a placeholder if no expenses
            label = ctk.CTkLabel(self.chart_frame, text="No expenses to display", text_color="gray")
            label.pack(pady=20)
            return

        # Create pie chart with dark mode
        fig = Figure(figsize=(5, 4), dpi=100, facecolor="#212121")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#212121")

        # Prepare data: expenses + leftover income
        chart_categories = list(category_totals.keys()) + ["Leftover Income"]
        chart_values = list(category_totals.values()) + [max(0, balance)]
        
        colors = ["#3b82f6", "#ef4444", "#10b981"]
        colors = colors[:len(chart_categories)]

        wedges, texts, autotexts = ax.pie(chart_values, labels=chart_categories, autopct="%1.1f%%", 
                                           colors=colors, startangle=90, textprops={"fontsize": 10, "color": "#e0e0e0"})
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")

        ax.set_title("Budget Breakdown", fontsize=12, fontweight="bold", color="#e0e0e0")

        # Embed matplotlib figure in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# --- Run GUI ---
if __name__ == "__main__":
    print("Launching GUI...")
    app = BudgetBuddyApp()
    app.mainloop()
