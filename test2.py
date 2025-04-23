import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# 🟢 ENTITY
class UserAccount:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

    @staticmethod
    def login(user_id, password, profile_type):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, user_type FROM users 
            WHERE username=? AND password=? AND user_type=?
        """, (user_id, password, profile_type))
        result = cursor.fetchone()
        conn.close()

        if result:
            return UserAccount(username=result[0], user_type=result[1])
        else:
            raise ValueError("Invalid credentials")

    @staticmethod
    def setup_database():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", ("admin", "admin", "Admin"))
        conn.commit()
        conn.close()

# 🔵 CONTROLLER
class UserLoginController:
    def login(self, user_id, password, profile_type):
        try:
            return UserAccount.login(user_id, password, profile_type)
        except ValueError as e:
            return str(e)

# 🟡 BOUNDARY
class UserLoginPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Login System BCE")
        self.root.geometry("400x200")

        # UI components
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(self.left_frame, text="Select User Type:").pack(anchor=tk.W)
        self.user_type = ttk.Combobox(self.left_frame, values=["Admin", "Cleaner", "Homeowner", "Platform Management"])
        self.user_type.current(0)
        self.user_type.pack()

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.right_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = tk.Entry(self.right_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.right_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = tk.Entry(self.right_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.right_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=5)

        self.logout_button = tk.Button(self.right_frame, text="Logout", state=tk.DISABLED, command=self.logout)
        self.logout_button.grid(row=2, column=1, pady=5)

        self.status_label = tk.Label(self.right_frame, text="Not logged in.", fg="gray")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        profile_type = self.user_type.get()

        result = self.controller.login(username, password, profile_type)

        if isinstance(result, UserAccount):
            self.status_label.config(text=f"Logged in as {result.user_type}: {result.username}", fg="green")
            self.login_button.config(state=tk.DISABLED)
            self.logout_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Failed", result)

    def logout(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="Not logged in.", fg="gray")
        self.login_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.DISABLED)

# 🎬 App start
if __name__ == "__main__":
    UserAccount.setup_database()  # Ensure DB is ready

    root = tk.Tk()
    controller = UserLoginController()
    app = UserLoginPage(root, controller)

    root.mainloop()
