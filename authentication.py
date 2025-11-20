"""
Login and Authentication Module
Handles user login, session management, and decryption key functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
from datetime import datetime, timedelta
from email_sender import EmailSender


class AuthenticationManager:
    def __init__(self):
        self.current_user = None
        self.session_file = "user_session.json"
        self.users_file = "users.json"
        self.email_sender = EmailSender()
        
    def hash_password(self, password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email, password, decryption_key):
        """Create a new user account."""
        try:
            # Load existing users
            users = self.load_users()
            
            # Check if user already exists
            if email in users:
                return False, "User already exists"
            
            # Validate email format
            if not self.email_sender.validate_email(email):
                return False, "Invalid email format"
            
            # Validate password length
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            
            # Validate decryption key length
            if len(decryption_key) < 4:
                return False, "Decryption key must be at least 4 characters"
            
            # Create user
            users[email] = {
                'password_hash': self.hash_password(password),
                'decryption_key': self.hash_password(decryption_key),
                'created_at': datetime.now().isoformat(),
                'last_login': None
            }
            
            # Save users
            self.save_users(users)
            return True, "User created successfully"
            
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    def authenticate_user(self, email, password):
        """Authenticate user login."""
        try:
            users = self.load_users()
            
            if email not in users:
                return False, "User not found"
            
            user = users[email]
            password_hash = self.hash_password(password)
            
            if user['password_hash'] != password_hash:
                return False, "Invalid password"
            
            # Update last login
            user['last_login'] = datetime.now().isoformat()
            users[email] = user
            self.save_users(users)
            
            # Set current user
            self.current_user = {
                'email': email,
                'decryption_key': user['decryption_key']
            }
            
            # Save session
            self.save_session()
            
            return True, "Login successful"
            
        except Exception as e:
            return False, f"Authentication error: {str(e)}"
    
    def verify_decryption_key(self, key):
        """Verify user's decryption key."""
        if not self.current_user:
            return False
        
        key_hash = self.hash_password(key)
        return key_hash == self.current_user['decryption_key']
    
    def load_users(self):
        """Load users from file."""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self, users):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_session(self):
        """Load user session."""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                session = json.load(f)
                
                # Check if session is still valid (24 hours)
                created_at = datetime.fromisoformat(session['created_at'])
                if datetime.now() - created_at < timedelta(hours=24):
                    self.current_user = session['user']
                    return True
                else:
                    # Session expired, remove file
                    os.remove(self.session_file)
        return False
    
    def save_session(self):
        """Save user session."""
        if self.current_user:
            session = {
                'user': self.current_user,
                'created_at': datetime.now().isoformat()
            }
            with open(self.session_file, 'w') as f:
                json.dump(session, f, indent=2)
    
    def logout(self):
        """Logout current user."""
        self.current_user = None
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
    
    def get_current_user(self):
        """Get current logged-in user."""
        return self.current_user


class LoginWindow:
    def __init__(self, parent, auth_manager, on_login_success):
        self.parent = parent
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        
        # Create login window
        self.login_window = tk.Toplevel(parent)
        self.login_window.title("Login - Secure Messaging")
        self.login_window.geometry("400x500")
        self.login_window.configure(bg='#f0f0f0')
        self.login_window.resizable(False, False)
        
        # Center the window
        self.login_window.transient(parent)
        self.login_window.grab_set()
        
        # Variables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.decryption_key_var = tk.StringVar()
        self.is_login_mode = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create login window widgets."""
        
        # Title
        title_label = tk.Label(
            self.login_window,
            text="🔐 Secure Messaging Login",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Mode selection
        mode_frame = tk.Frame(self.login_window, bg='#f0f0f0')
        mode_frame.pack(pady=10)
        
        login_radio = tk.Radiobutton(
            mode_frame, text="Login", variable=self.is_login_mode, value=True,
            command=self.toggle_mode, bg='#f0f0f0', font=("Arial", 10)
        )
        login_radio.pack(side='left', padx=10)
        
        register_radio = tk.Radiobutton(
            mode_frame, text="Register", variable=self.is_login_mode, value=False,
            command=self.toggle_mode, bg='#f0f0f0', font=("Arial", 10)
        )
        register_radio.pack(side='left', padx=10)
        
        # Main form frame
        form_frame = tk.Frame(self.login_window, bg='#f0f0f0')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Email
        tk.Label(form_frame, text="Email:", bg='#f0f0f0', font=("Arial", 10)).pack(anchor='w')
        email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=40)
        email_entry.pack(pady=(5, 15))
        
        # Password
        tk.Label(form_frame, text="Password:", bg='#f0f0f0', font=("Arial", 10)).pack(anchor='w')
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, show='*', width=40)
        password_entry.pack(pady=(5, 15))
        
        # Decryption Key
        self.decryption_key_label = tk.Label(form_frame, text="Decryption Key:", bg='#f0f0f0', font=("Arial", 10))
        self.decryption_key_label.pack(anchor='w')
        self.decryption_key_entry = ttk.Entry(form_frame, textvariable=self.decryption_key_var, show='*', width=40)
        self.decryption_key_entry.pack(pady=(5, 15))
        
        # Action button
        self.action_button = ttk.Button(form_frame, text="Login", command=self.handle_action)
        self.action_button.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(form_frame, text="", bg='#f0f0f0', fg='blue')
        self.status_label.pack(pady=5)
        
        # Info text
        info_text = """
🔑 Decryption Key: Used to encrypt/decrypt your messages
📧 Email: Your Gmail address for sending messages
🔒 Password: Your account password (not Gmail password)
        """
        info_label = tk.Label(
            form_frame, text=info_text, bg='#f0f0f0', 
            fg='gray', font=("Arial", 8), justify='left'
        )
        info_label.pack(pady=10)
        
        # Set initial mode
        self.toggle_mode()
        
    def toggle_mode(self):
        """Toggle between login and register modes."""
        if self.is_login_mode.get():
            self.action_button.config(text="Login")
            self.decryption_key_label.config(text="Decryption Key:")
            self.status_label.config(text="Enter your credentials to login")
        else:
            self.action_button.config(text="Register")
            self.decryption_key_label.config(text="Decryption Key (choose a secure key):")
            self.status_label.config(text="Create a new account")
    
    def handle_action(self):
        """Handle login or register action."""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        decryption_key = self.decryption_key_var.get().strip()
        
        if not all([email, password, decryption_key]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.is_login_mode.get():
            # Login
            success, message = self.auth_manager.authenticate_user(email, password)
            if success:
                # Verify decryption key
                if self.auth_manager.verify_decryption_key(decryption_key):
                    self.status_label.config(text="Login successful!", fg='green')
                    self.login_window.after(1000, self.close_and_login)
                else:
                    self.status_label.config(text="Invalid decryption key", fg='red')
            else:
                self.status_label.config(text=message, fg='red')
        else:
            # Register
            success, message = self.auth_manager.create_user(email, password, decryption_key)
            if success:
                self.status_label.config(text="Account created successfully!", fg='green')
                self.login_window.after(1000, self.close_and_login)
            else:
                self.status_label.config(text=message, fg='red')
    
    def close_and_login(self):
        """Close login window and call success callback."""
        self.login_window.destroy()
        self.on_login_success()


# Test function
if __name__ == "__main__":
    auth = AuthenticationManager()
    
    # Test user creation
    success, msg = auth.create_user("test@gmail.com", "password123", "mykey123")
    print(f"Create user: {success} - {msg}")
    
    # Test authentication
    success, msg = auth.authenticate_user("test@gmail.com", "password123")
    print(f"Authenticate: {success} - {msg}")
    
    # Test decryption key
    valid = auth.verify_decryption_key("mykey123")
    print(f"Decryption key valid: {valid}")
    
    print("Authentication module loaded successfully!")
