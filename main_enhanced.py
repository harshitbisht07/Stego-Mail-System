"""
Enhanced Main GUI Application for Image-Based Secure Messaging
Now includes login system, session management, and encryption keys.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import tempfile
from datetime import datetime
from steganography import Steganography
from email_sender import EmailSender
from authentication import AuthenticationManager, LoginWindow


class SecureMessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image-Based Secure Messaging")
        self.root.geometry("900x750")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize modules
        self.stego = Steganography()
        self.email_sender = EmailSender()
        self.auth_manager = AuthenticationManager()
        
        # Variables
        self.selected_image_path = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.secret_message = tk.StringVar()
        self.is_logged_in = False
        
        # Check for existing session
        if self.auth_manager.load_session():
            self.is_logged_in = True
            self.create_main_interface()
        else:
            self.show_login()
        
    def show_login(self):
        """Show login window."""
        # Hide main window temporarily
        self.root.withdraw()
        
        # Create login window
        login_window = LoginWindow(self.root, self.auth_manager, self.on_login_success)
        
        # Center login window
        login_window.login_window.update_idletasks()
        x = (login_window.login_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (login_window.login_window.winfo_screenheight() // 2) - (500 // 2)
        login_window.login_window.geometry(f"400x500+{x}+{y}")
        
    def on_login_success(self):
        """Handle successful login."""
        self.is_logged_in = True
        self.root.deiconify()  # Show main window
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main application interface."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        
        # Title with user info
        user_info = self.auth_manager.get_current_user()
        title_text = f"🔐 Image-Based Secure Messaging - Welcome, {user_info['email']}"
        title_label = tk.Label(
            self.root, 
            text=title_text, 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Logout button
        logout_frame = tk.Frame(self.root, bg='#f0f0f0')
        logout_frame.pack(pady=5)
        logout_btn = ttk.Button(logout_frame, text="🚪 Logout", command=self.logout)
        logout_btn.pack(side='right')
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Send Message Tab
        send_frame = ttk.Frame(notebook)
        notebook.add(send_frame, text="📤 Send Secret Message")
        self.create_send_tab(send_frame)
        
        # Decode Message Tab
        decode_frame = ttk.Frame(notebook)
        notebook.add(decode_frame, text="🔍 Decode Secret Message")
        self.create_decode_tab(decode_frame)
        
        # Settings Tab
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        self.create_settings_tab(settings_frame)
        
    def create_send_tab(self, parent):
        """Create the send message tab."""
        
        # Email Setup Section
        email_frame = ttk.LabelFrame(parent, text="📧 Email Setup", padding=10)
        email_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(email_frame, text="Gmail App Password:").grid(row=0, column=0, sticky='w', pady=2)
        self.app_password_var = tk.StringVar()
        app_password_entry = ttk.Entry(email_frame, textvariable=self.app_password_var, show='*', width=40)
        app_password_entry.grid(row=0, column=1, padx=5, pady=2)
        
        test_btn = ttk.Button(email_frame, text="Test Connection", command=self.test_connection)
        test_btn.grid(row=0, column=2, padx=5, pady=2)
        
        # Image Selection Section
        image_frame = ttk.LabelFrame(parent, text="🖼️ Select Image", padding=10)
        image_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(image_frame, text="Image File:").grid(row=0, column=0, sticky='w', pady=2)
        image_entry = ttk.Entry(image_frame, textvariable=self.selected_image_path, width=40)
        image_entry.grid(row=0, column=1, padx=5, pady=2)
        
        browse_btn = ttk.Button(image_frame, text="Browse", command=self.browse_image)
        browse_btn.grid(row=0, column=2, padx=5, pady=2)
        
        # Image Info
        self.image_info_label = tk.Label(image_frame, text="", fg='blue')
        self.image_info_label.grid(row=1, column=0, columnspan=3, pady=2)
        
        # Message Section
        message_frame = ttk.LabelFrame(parent, text="💬 Secret Message", padding=10)
        message_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(message_frame, text="Enter your secret message:").pack(anchor='w')
        self.message_text = scrolledtext.ScrolledText(message_frame, height=6, width=60)
        self.message_text.pack(fill='both', expand=True, pady=5)
        
        # Recipient Section
        recipient_frame = ttk.LabelFrame(parent, text="📧 Recipient", padding=10)
        recipient_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(recipient_frame, text="Recipient Email:").grid(row=0, column=0, sticky='w', pady=2)
        recipient_entry = ttk.Entry(recipient_frame, textvariable=self.recipient_email, width=40)
        recipient_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Send Button
        send_btn = ttk.Button(parent, text="🚀 Send Secret Message", command=self.send_secret_message)
        send_btn.pack(pady=20)
        
        # Status
        self.status_label = tk.Label(parent, text="Ready to send secret message", fg='green')
        self.status_label.pack(pady=5)
        
    def create_decode_tab(self, parent):
        """Create the decode message tab."""
        
        # Image Selection
        decode_image_frame = ttk.LabelFrame(parent, text="🖼️ Select Encoded Image", padding=10)
        decode_image_frame.pack(fill='x', padx=10, pady=5)
        
        self.decode_image_path = tk.StringVar()
        tk.Label(decode_image_frame, text="Image File:").grid(row=0, column=0, sticky='w', pady=2)
        decode_image_entry = ttk.Entry(decode_image_frame, textvariable=self.decode_image_path, width=40)
        decode_image_entry.grid(row=0, column=1, padx=5, pady=2)
        
        decode_browse_btn = ttk.Button(decode_image_frame, text="Browse", command=self.browse_decode_image)
        decode_browse_btn.grid(row=0, column=2, padx=5, pady=2)
        
        # Decode Button
        decode_btn = ttk.Button(parent, text="🔍 Decode Secret Message", command=self.decode_secret_message)
        decode_btn.pack(pady=20)
        
        # Decoded Message Display
        decode_result_frame = ttk.LabelFrame(parent, text="📝 Decoded Message", padding=10)
        decode_result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.decoded_message_text = scrolledtext.ScrolledText(decode_result_frame, height=10, width=60)
        self.decoded_message_text.pack(fill='both', expand=True)
        
        # Decode Status
        self.decode_status_label = tk.Label(parent, text="Select an encoded image to decode", fg='blue')
        self.decode_status_label.pack(pady=5)
        
    def create_settings_tab(self, parent):
        """Create the settings tab."""
        
        # User Info Section
        user_frame = ttk.LabelFrame(parent, text="👤 User Information", padding=10)
        user_frame.pack(fill='x', padx=10, pady=5)
        
        user_info = self.auth_manager.get_current_user()
        tk.Label(user_frame, text=f"Email: {user_info['email']}", font=("Arial", 10)).pack(anchor='w')
        
        # Security Info
        security_frame = ttk.LabelFrame(parent, text="🔒 Security Information", padding=10)
        security_frame.pack(fill='x', padx=10, pady=5)
        
        security_text = """
🔑 Your messages are encrypted with your personal decryption key
🖼️ Messages are hidden in images using LSB steganography
📧 Images are sent via secure SMTP
🔐 Only you can decrypt messages with your key

Security Features:
• End-to-end encryption
• Steganographic hiding
• Secure email transmission
• Session management
        """
        security_label = tk.Label(security_frame, text=security_text, justify='left', font=("Arial", 9))
        security_label.pack(anchor='w')
        
        # Instructions
        instructions_frame = ttk.LabelFrame(parent, text="📖 Instructions", padding=10)
        instructions_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        instructions_text = """
How to Send a Secret Message:
1. Enter your Gmail App Password
2. Test the connection
3. Select an image file
4. Type your secret message
5. Enter recipient's email
6. Click "Send Secret Message"

How to Decode a Message:
1. Go to "Decode Secret Message" tab
2. Select the encoded image
3. Click "Decode Secret Message"
4. Your decryption key will be used automatically

Important Notes:
• Use Gmail App Password (not regular password)
• Keep your decryption key secure
• Larger images can hold longer messages
• Messages are encrypted before hiding in images
        """
        instructions_label = tk.Label(instructions_frame, text=instructions_text, justify='left', font=("Arial", 9))
        instructions_label.pack(anchor='w')
        
    def browse_image(self):
        """Browse for image file."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.selected_image_path.set(filename)
            self.show_image_info(filename)
            
    def browse_decode_image(self):
        """Browse for encoded image file."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.decode_image_path.set(filename)
            
    def show_image_info(self, image_path):
        """Show information about the selected image."""
        info = self.stego.get_image_info(image_path)
        if info:
            text = f"Size: {info['size'][0]}x{info['size'][1]} | Mode: {info['mode']} | File Size: {info['file_size']} bytes"
            self.image_info_label.config(text=text)
        else:
            self.image_info_label.config(text="Error reading image info")
            
    def test_connection(self):
        """Test email connection."""
        email = self.auth_manager.get_current_user()['email']
        password = self.app_password_var.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter your Gmail App Password")
            return
            
        self.status_label.config(text="Testing connection...", fg='orange')
        self.root.update()
        
        if self.email_sender.test_connection(email, password):
            self.status_label.config(text="Connection successful!", fg='green')
            messagebox.showinfo("Success", "Email connection test successful!")
        else:
            self.status_label.config(text="Connection failed", fg='red')
            messagebox.showerror("Error", "Connection test failed. Please check your App Password.")
            
    def send_secret_message(self):
        """Send the secret message."""
        # Validate inputs
        if not all([self.app_password_var.get(), self.selected_image_path.get(), self.recipient_email.get()]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a secret message")
            return
            
        if not self.email_sender.validate_email(self.recipient_email.get()):
            messagebox.showerror("Error", "Invalid recipient email format")
            return
            
        # Get user's decryption key
        user_info = self.auth_manager.get_current_user()
        decryption_key = user_info['decryption_key']
        
        # Create temporary file for encoded image
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        encoded_image_path = os.path.join(temp_dir, f"secret_image_{timestamp}.png")
        
        try:
            # Encode message with encryption
            self.status_label.config(text="Encoding and encrypting message...", fg='orange')
            self.root.update()
            
            success = self.stego.encode_message(
                self.selected_image_path.get(),
                message,
                encoded_image_path,
                decryption_key  # Use user's decryption key for encryption
            )
            
            if not success:
                messagebox.showerror("Error", "Failed to encode message in image")
                return
                
            # Send email
            self.status_label.config(text="Sending email...", fg='orange')
            self.root.update()
            
            success = self.email_sender.send_encoded_image(
                self.auth_manager.get_current_user()['email'],
                self.app_password_var.get(),
                self.recipient_email.get(),
                encoded_image_path,
                "Secret Image Message",
                "Please find the attached image with a hidden message. Use the decode feature to extract it."
            )
            
            if success:
                self.status_label.config(text="Secret message sent successfully!", fg='green')
                messagebox.showinfo("Success", "Secret message sent successfully!")
                
                # Clear form
                self.message_text.delete("1.0", tk.END)
                self.recipient_email.set("")
            else:
                self.status_label.config(text="Failed to send message", fg='red')
                messagebox.showerror("Error", "Failed to send email")
                
        except Exception as e:
            self.status_label.config(text="Error occurred", fg='red')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(encoded_image_path):
                try:
                    os.remove(encoded_image_path)
                except:
                    pass
                    
    def decode_secret_message(self):
        """Decode secret message from image."""
        image_path = self.decode_image_path.get()
        
        if not image_path:
            messagebox.showerror("Error", "Please select an image file")
            return
            
        if not os.path.exists(image_path):
            messagebox.showerror("Error", "Image file does not exist")
            return
            
        try:
            self.decode_status_label.config(text="Decoding message...", fg='orange')
            self.root.update()
            
            # Get user's decryption key
            user_info = self.auth_manager.get_current_user()
            decryption_key = user_info['decryption_key']
            
            decoded_message = self.stego.decode_message(image_path, decryption_key)
            
            if decoded_message:
                self.decoded_message_text.delete("1.0", tk.END)
                self.decoded_message_text.insert("1.0", decoded_message)
                self.decode_status_label.config(text="Message decoded successfully!", fg='green')
            else:
                self.decode_status_label.config(text="No message found or decode failed", fg='red')
                messagebox.showwarning("Warning", "No secret message found in the image or decode failed")
                
        except Exception as e:
            self.decode_status_label.config(text="Error occurred", fg='red')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def logout(self):
        """Logout current user."""
        self.auth_manager.logout()
        self.is_logged_in = False
        
        # Clear the main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show login again
        self.show_login()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = SecureMessagingApp(root)
    
    # Add some styling
    style = ttk.Style()
    style.theme_use('clam')
    
    root.mainloop()


if __name__ == "__main__":
    main()





