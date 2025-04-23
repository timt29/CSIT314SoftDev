import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ENTITY
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
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", ("admin", "admin", "Admin"))
        self.conn.commit()

    def validate_user(self, username, password, user_type):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND user_type=?",
            (username, password, user_type)
        )
        return self.cursor.fetchone()

    def create_user(self, username, password, user_type):
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, user_type))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self):
        self.conn.close()

# CONTROLLER
class AuthController:
    def __init__(self, repo):
        self.repo = repo

    def login(self, username, password, user_type):
        return self.repo.validate_user(username, password, user_type)

    def register_user(self, username, password, user_type):
        return self.repo.create_user(username, password, user_type)

# UI
class LoginApp:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Login Portal")
        self.root.geometry("700x400")
        self.root.configure(bg="gray20")

        # Header
        header = tk.Label(root, text="Website Name", font=("Arial", 18, "bold"), bg="gray60")
        header.pack(fill=tk.X, pady=(0, 10))

        # Layout frames
        container = tk.Frame(root, bg="gray70", padx=20, pady=20)
        container.pack(expand=True)

        left_frame = tk.Frame(container, bg="gray70")
        right_frame = tk.Frame(container, bg="gray70")
        left_frame.pack(side=tk.LEFT, padx=30)
        right_frame.pack(side=tk.RIGHT, padx=30)

        # LEFT SIDE: Role selection
        tk.Label(left_frame, text="Login as", font=("Arial", 12), bg="gray70").pack(anchor=tk.W, pady=(0, 5))
        self.user_type = ttk.Combobox(left_frame, values=["Admin", "Platform Manager", "Homeowner", "Cleaner"], state="readonly")
        self.user_type.current(0)
        self.user_type.pack()

        # RIGHT SIDE: Credentials
        tk.Label(right_frame, text="Username:", font=("Arial", 12), bg="gray70").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = tk.Entry(right_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(right_frame, text="Password:", font=("Arial", 12), bg="gray70").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = tk.Entry(right_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(right_frame, text="Log in", command=self.login, bg="lightpink", width=10)
        self.login_button.grid(row=2, column=1, sticky=tk.W, pady=10)

        self.status_label = tk.Label(right_frame, text="", font=("Arial", 10), bg="gray70", fg="red")
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.admin_button = tk.Button(right_frame, text="Open Admin Panel", command=self.open_admin_panel, state=tk.DISABLED, bg="lightgray")
        self.admin_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type.get()

        if self.controller.login(username, password, user_type):
            self.status_label.config(text=f"Logged in as {user_type}: {username}", fg="green")
            if user_type == "Admin":
                self.admin_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Invalid login. Please check credentials.", fg="red")

    def open_admin_panel(self):
        AdminPanel(self.controller)

# Admin Panel
class AdminPanel:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Toplevel()
        self.window.title("Admin Panel - Create New User")
        self.window.geometry("400x250")

        tk.Label(self.window, text="New Username:").pack()
        self.new_username = tk.Entry(self.window)
        self.new_username.pack()

        tk.Label(self.window, text="New Password:").pack()
        self.new_password = tk.Entry(self.window, show="*")
        self.new_password.pack()

        tk.Label(self.window, text="User Type:").pack()
        self.user_type = ttk.Combobox(self.window, values=["Cleaner", "Homeowner", "Platform Manager"])
        self.user_type.current(0)
        self.user_type.pack()

        tk.Button(self.window, text="Create User", command=self.create_user).pack(pady=10)
        self.status_label = tk.Label(self.window, text="", fg="blue")
        self.status_label.pack()

    def create_user(self):
        uname = self.new_username.get()
        pwd = self.new_password.get()
        role = self.user_type.get()

        if not uname or not pwd:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        if self.controller.register_user(uname, pwd, role):
            self.status_label.config(text=f"User '{uname}' created!", fg="green")
        else:
            self.status_label.config(text="Username already exists.", fg="red")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    repo = UserRepository()
    controller = AuthController(repo)
    app = LoginApp(root, controller)

    def on_close():
        repo.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
