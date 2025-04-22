import tkinter as tk
from tkinter import ttk, messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Login/Logout")
        self.root.geometry("400x200")

        # Left panel for user type selection
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)

        tk.Label(self.left_frame, text="Select User Type:").pack(anchor=tk.W)
        self.user_type = ttk.Combobox(self.left_frame, values=[
            "Admin", "Cleaner", "Homeowner", "Platform Management"
        ])
        self.user_type.current(0)
        self.user_type.pack()

        # Right panel for login credentials
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

        if username and password:
            self.status_label.config(text=f"Logged in as {user_type}: {username}", fg="green")
            self.login_button.config(state=tk.DISABLED)
            self.logout_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Login Failed", "Please enter both username and password.")

    def logout(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="Not logged in.", fg="gray")
        self.login_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.DISABLED)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
