import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog  # Add this import statement
import random
import os

# File to save user data
USER_DATA_FILE = "user_data.txt"

class MiniCasinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Mini Casino - Guess the Number Edition")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c1c")  # Dark background for a casino feel

        self.username = ""
        self.password = ""
        self.balance = 0
        self.high_score = 0
        self.money_earned = 0
        self.max_number = 3

        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title with a glowing effect
        title_label = tk.Label(self.root, text="🎰 Mini Casino Login", font=("Arial", 18, "bold"), fg="#ffd700", bg="#1c1c1c")
        title_label.pack(pady=30)

        tk.Label(self.root, text="Username:", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=20)
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", font=("Arial", 14), command=self.login, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        login_button.pack(pady=10)

        create_account_button = tk.Button(self.root, text="Create Account", font=("Arial", 14), command=self.create_account, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        create_account_button.pack(pady=5)

    def create_account(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="🎰 Create New Account", font=("Arial", 18, "bold"), fg="#ffd700", bg="#1c1c1c")
        title_label.pack(pady=30)

        tk.Label(self.root, text="Username:", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack()
        self.new_username_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack()
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=20)
        self.new_password_entry.pack(pady=5)

        tk.Label(self.root, text="Starting Balance ($):", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack(pady=10)
        self.new_balance_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.new_balance_entry.pack(pady=5)

        create_button = tk.Button(self.root, text="Create Account", font=("Arial", 14), command=self.save_new_account, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        create_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back to Login", font=("Arial", 14), command=self.create_login_screen, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        back_button.pack(pady=5)

    def save_new_account(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        balance = self.new_balance_entry.get().strip()

        if not username or not password or not balance:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if self.check_user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return

        try:
            balance = int(balance)
            if balance <= 0:
                raise ValueError("Balance must be greater than zero.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        with open(USER_DATA_FILE, "a") as file:
            file.write(f"{username},{password},{balance},{balance},0\n")  # Username, password, balance, high score, money earned
        messagebox.showinfo("Success", "Account created successfully! You can now log in.")
        self.create_login_screen()

    def check_user_exists(self, username):
        if not os.path.exists(USER_DATA_FILE):
            return False
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                if line.split(",")[0] == username:
                    return True
        return False

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        user_data = self.get_user_data(username)

        if user_data and user_data[1] == password:
            self.username = username
            self.password = password
            self.balance = int(user_data[2])
            self.high_score = int(user_data[3])
            self.money_earned = int(user_data[4])
            self.create_game_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def get_user_data(self, username):
        if not os.path.exists(USER_DATA_FILE):
            return None
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                user_data = line.strip().split(",")
                if user_data[0] == username:
                    return user_data
        return None

    def create_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="🎲 Guess the Number!", font=("Arial", 18, "bold"), fg="#ffd700", bg="#1c1c1c")
        title_label.pack(pady=30)

        self.balance_label = tk.Label(self.root, text=f"💰 Balance: ${self.balance}", font=("Arial", 14), fg="#ffffff", bg="#1c1c1c")
        self.balance_label.pack()

        self.high_score_label = tk.Label(self.root, text=f"🏆 High Score: ${self.high_score}", font=("Arial", 14), fg="#ffffff", bg="#1c1c1c")
        self.high_score_label.pack()

        tk.Label(self.root, text="Your Bet Amount ($):", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack(pady=10)
        self.bet_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.bet_entry.pack()

        tk.Label(self.root, text=f"Guess a number (1 to {self.max_number}):", font=("Arial", 12), fg="#ffffff", bg="#1c1c1c").pack(pady=5)
        self.guess_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.guess_entry.pack()

        self.result_label = tk.Label(self.root, text="", fg="blue", font=("Arial", 12))
        self.result_label.pack(pady=10)

        submit_button = tk.Button(self.root, text="Submit Guess", font=("Arial", 14), command=self.submit_guess, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        submit_button.pack(pady=5)

        quit_button = tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.quit_game, bg="#ffd700", fg="#1c1c1c", relief="solid", width=15)
        quit_button.pack(pady=10)

    def submit_guess(self):
        try:
            bet = int(self.bet_entry.get())
            guess = int(self.guess_entry.get())
            if bet <= 0 or bet > self.balance:
                raise ValueError("Invalid bet amount.")
            if guess < 1 or guess > self.max_number:
                raise ValueError("Invalid guess.")

            number = random.randint(1, self.max_number)
            if guess == number:
                self.balance += bet
                self.money_earned += bet
                self.result_label.config(text=f"🎉 Correct! It was {number}. You won ${bet}!", fg="green")
            else:
                self.balance -= bet
                self.result_label.config(text=f"❌ Wrong! It was {number}. You lost ${bet}.", fg="red")

            if self.balance > self.high_score:
                self.high_score = self.balance

            self.update_labels()
            self.save_user_data()
            self.check_game_over()

        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))

    def update_labels(self):
        self.balance_label.config(text=f"💰 Balance: ${self.balance}")
        self.high_score_label.config(text=f"🏆 High Score: ${self.high_score}")

    def save_user_data(self):
        lines = []
        with open(USER_DATA_FILE, "r") as file:
            lines = file.readlines()

        with open(USER_DATA_FILE, "w") as file:
            for line in lines:
                user_data = line.strip().split(",")
                if user_data[0] == self.username:
                    file.write(f"{self.username},{self.password},{self.balance},{self.high_score},{self.money_earned}\n")
                else:
                    file.write(line)

    def check_game_over(self):
        if self.balance <= 0:
            response = messagebox.askyesno("Game Over", "You're out of money! Would you like to add more funds?")
            if response:
                self.add_money()
            else:
                messagebox.showinfo("Thank You", f"You walked away with ${self.balance}.\n🏆 High Score: ${self.high_score}")
                self.create_login_screen()

    def add_money(self):
        add_amount = tk.simpledialog.askinteger("Add Funds", "How much would you like to add?", minvalue=1, maxvalue=10000)
        if add_amount:
            self.balance += add_amount
            self.save_user_data()
            messagebox.showinfo("Funds Added", f"${add_amount} has been added to your account.")
            self.update_labels()

    def quit_game(self):
        messagebox.showinfo("Thank You", f"You walked away with ${self.balance}.\n🏆 High Score: ${self.high_score}")
        self.root.destroy()

# Run the game
root = tk.Tk()
game = MiniCasinoGUI(root)
root.mainloop()
