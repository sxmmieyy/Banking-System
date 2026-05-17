import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class SimpleBankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Bank - PH Peso Edition")
        self.root.geometry("550x550")
        
        self.balance_file = "balance.txt"
        self.history_file = "history.txt"
        
        self.balance = self.load_balance_from_file()
        
        self.lbl_balance = tk.Label(root, text=f"Balance: \u20b1{self.balance:,.2f}", font=("Arial", 20, "bold"), fg="green")
        self.lbl_balance.pack(pady=15)
        
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)
        
        tk.Label(frame_input, text="Amount: \u20b1", font=("Arial", 12)).grid(row=0, column=0)
        self.ent_amount = tk.Entry(frame_input, font=("Arial", 12), width=15)
        self.ent_amount.grid(row=0, column=1, padx=5)
        self.ent_amount.focus()

        frame_btns = tk.Frame(root)
        frame_btns.pack(pady=10)
        
        tk.Button(frame_btns, text="Deposit", font=("Arial", 11), bg="#4CAF50", fg="white", width=10, command=self.deposit).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Withdraw", font=("Arial", 11), bg="#f44336", fg="white", width=10, command=self.withdraw).pack(side=tk.RIGHT, padx=5)
        
        frame_history_header = tk.Frame(root)
        frame_history_header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(frame_history_header, text="Transaction History", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        tk.Button(frame_history_header, text="Clear History", font=("Arial", 9), bg="#757575", fg="white", command=self.clear_history).pack(side=tk.RIGHT)
        
        self.table = ttk.Treeview(root, columns=("DateTime", "Action", "Amount", "Balance"), show="headings", height=10)
        self.table.heading("DateTime", text="Date & Time")
        self.table.heading("Action", text="Action")
        self.table.heading("Amount", text="Amount")
        self.table.heading("Balance", text="Available Balance")
        
        self.table.column("DateTime", width=150, anchor=tk.CENTER)
        self.table.column("Action", width=100, anchor=tk.CENTER)
        self.table.column("Amount", width=100, anchor=tk.E)
        self.table.column("Balance", width=120, anchor=tk.E)
        self.table.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.refresh_table_display()

    def load_balance_from_file(self):
        try:
            if os.path.exists(self.balance_file):
                with open(self.balance_file, "r", encoding="utf-8") as f:
                    return float(f.read().strip())
        except Exception:
            pass
        return 0.0

    def save_data_to_files(self, action, amount):
        try:
            with open(self.balance_file, "w", encoding="utf-8") as f:
                f.write(f"{self.balance:.2f}")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp},{action},\u20b1{amount:.2f},\u20b1{self.balance:.2f}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def get_clean_amount(self):
        raw = self.ent_amount.get().strip()
        if not raw:
            messagebox.showwarning("Warning", "Please enter an amount.")
            return None
        
        clean = raw.replace("\u20b1", "").replace("PHP", "").replace("php", "").replace("$", "").replace(",", "").strip()
        try:
            val = float(clean)
            if val <= 0:
                messagebox.showwarning("Warning", "Amount must be greater than zero.")
                return None
            return val
        except ValueError:
            messagebox.showerror("Invalid Input", f"'{raw}' is not a valid number.")
            return None

    def deposit(self):
        amt = self.get_clean_amount()
        if amt is None: return
        
        self.balance += amt
        self.lbl_balance.config(text=f"Balance: \u20b1{self.balance:,.2f}")
        self.save_data_to_files("DEPOSIT", amt)
        self.refresh_table_display()
        self.ent_amount.delete(0, tk.END)

    def withdraw(self):
        amt = self.get_clean_amount()
        if amt is None: return
        
        if amt > self.balance:
            messagebox.showerror("Denied", "Insufficient funds! Action canceled.")
            return
        
        self.balance -= amt
        self.lbl_balance.config(text=f"Balance: \u20b1{self.balance:,.2f}")
        self.save_data_to_files("WITHDRAWAL", amt)
        self.refresh_table_display()
        self.ent_amount.delete(0, tk.END)

    def refresh_table_display(self):
        for row in self.table.get_children():
            self.table.delete(row)
            
        if not os.path.exists(self.history_file):
            return
            
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if line.strip():
                        parts = line.strip().split(",")
                        if len(parts) == 4:
                            self.table.insert("", tk.END, values=parts)
        except Exception:
            pass

    def clear_history(self):
        if not os.path.exists(self.history_file):
            messagebox.showinfo("Info", "History is already completely empty.")
            return

        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to permanently delete all transaction history?")
        if confirm:
            try:
                os.remove(self.history_file)
                self.refresh_table_display()
                messagebox.showinfo("Success", "Transaction history has been wiped clean!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear history file: {e}")

if __name__ == "__main__":
    window = tk.Tk()
    app = SimpleBankingApp(window)
    window.mainloop()