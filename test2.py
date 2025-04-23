import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# 🟢 ENTITY: User model and database access
class UserRepository:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_user_table()

    def _create_user_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
        """)
        # Default user
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", ("admin", "admin", "Admin"))
        self.conn.commit()

    def validate_user(self, username, password, user_type):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND user_type=?",
            (username, password, user_type)
        )
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

# 🔵 CONTROLLER: Business logic between UI and Entity
class AuthController:
    def __init__(self, user_repository):
        self.user_repo = user_repository

    def login(self, username, password, user_type):
        return self.user_repo.validate_user(username, password, user_type)

# 🟡 BOUNDARY: UI
class LoginApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Login App (BCE)")
        self.root.geometry("400x200")

        # UI Layout
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
        user_type = self.user_type.get()

        if self.controller.login(username, password, user_type):
            self.status_label.config(text=f"Logged in as {user_type}: {username}", fg="green")
            self.login_button.config(state=tk.DISABLED)
            self.logout_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Failed", "Invalid username, password, or user type.")

    def logout(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="Not logged in.", fg="gray")
        self.login_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.DISABLED)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    repo = UserRepository()
    controller = AuthController(repo)
    app = LoginApp(root, controller)

    def on_closing():
        repo.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
