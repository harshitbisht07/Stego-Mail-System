"""
Main GUI Application for Image-Based Secure Messaging
Integrates steganography and email functionality with a user-friendly interface.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import tempfile
from datetime import datetime
from steganography import Steganography
from email_sender import EmailSender


class SecureMessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image-Based Secure Messaging")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize modules
        self.stego = Steganography()
        self.email_sender = EmailSender()
        
        # Variables
        self.selected_image_path = tk.StringVar()
        self.sender_email = tk.StringVar()
        self.sender_password = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.secret_message = tk.StringVar()
        self.encryption_key = tk.StringVar()
        self.decryption_key = tk.StringVar()
        self.crypto_key = tk.StringVar()
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🔐 Image-Based Secure Messaging", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
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
        
    def create_send_tab(self, parent):
        """Create the send message tab."""
        
        # Login Section
        login_frame = ttk.LabelFrame(parent, text="🔑 Login Credentials", padding=10)
        login_frame.pack(fill='x', padx=10, pady=5)
        
        # Email
        tk.Label(login_frame, text="Your Email:").grid(row=0, column=0, sticky='w', pady=2)
        email_entry = ttk.Entry(login_frame, textvariable=self.sender_email, width=40)
        email_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # App Password
        tk.Label(login_frame, text="App Password:").grid(row=1, column=0, sticky='w', pady=2)
        password_entry = ttk.Entry(login_frame, textvariable=self.sender_password, show='*', width=40)
        password_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Test Connection Button
        test_btn = ttk.Button(login_frame, text="Test Connection", command=self.test_connection)
        test_btn.grid(row=2, column=1, pady=5, sticky='e')
        
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
        
        # Encryption Key Section
        encryption_frame = ttk.LabelFrame(parent, text="🔑 Encryption Key", padding=10)
        encryption_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(encryption_frame, text="Encryption Key:").grid(row=0, column=0, sticky='w', pady=2)
        encryption_entry = ttk.Entry(encryption_frame, textvariable=self.encryption_key, show='*', width=40)
        encryption_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(encryption_frame, text="⚠️ Remember this key! You'll need it to decode the message.", 
                fg='orange', font=("Arial", 8)).grid(row=1, column=0, columnspan=2, sticky='w', pady=2)
        
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
        
        # Decryption Key Section
        decryption_frame = ttk.LabelFrame(parent, text="🔑 Decryption Key", padding=10)
        decryption_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(decryption_frame, text="Decryption Key:").grid(row=0, column=0, sticky='w', pady=2)
        decryption_entry = ttk.Entry(decryption_frame, textvariable=self.decryption_key, show='*', width=40)
        decryption_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(decryption_frame, text="⚠️ Enter the same key used to encrypt the message.", 
                fg='orange', font=("Arial", 8)).grid(row=1, column=0, columnspan=2, sticky='w', pady=2)
        
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
        email = self.sender_email.get()
        password = self.sender_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
            
        if not self.email_sender.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
            
        self.status_label.config(text="Testing connection...", fg='orange')
        self.root.update()
        
        if self.email_sender.test_connection(email, password):
            self.status_label.config(text="Connection successful!", fg='green')
            messagebox.showinfo("Success", "Email connection test successful!")
        else:
            self.status_label.config(text="Connection failed", fg='red')
            messagebox.showerror("Error", "Connection test failed. Please check your credentials.")
            
    def send_secret_message(self):
        """Send the secret message."""
        # Validate inputs
        if not all([self.sender_email.get(), self.sender_password.get(), 
                   self.selected_image_path.get(), self.recipient_email.get()]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a secret message")
            return
            
        encryption_key = self.encryption_key.get().strip()
        if not encryption_key:
            messagebox.showerror("Error", "Please enter an encryption key")
            return
            
        if len(encryption_key) < 4:
            messagebox.showerror("Error", "Encryption key must be at least 4 characters long")
            return
            
        if not self.email_sender.validate_email(self.recipient_email.get()):
            messagebox.showerror("Error", "Invalid recipient email format")
            return
            
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
                encryption_key  # Pass encryption key
            )
            
            if not success:
                messagebox.showerror("Error", "Failed to encode message in image")
                return
                
            # Send email
            self.status_label.config(text="Sending email...", fg='orange')
            self.root.update()
            
            success = self.email_sender.send_encoded_image(
                self.sender_email.get(),
                self.sender_password.get(),
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
            
        decryption_key = self.decryption_key.get().strip()
        if not decryption_key:
            messagebox.showerror("Error", "Please enter the decryption key")
            return
            
        try:
            self.decode_status_label.config(text="Decoding and decrypting message...", fg='orange')
            self.root.update()
            
            decoded_message = self.stego.decode_message(image_path, decryption_key)
            
            if decoded_message:
                self.decoded_message_text.delete("1.0", tk.END)
                self.decoded_message_text.insert("1.0", decoded_message)
                self.decode_status_label.config(text="Message decoded successfully!", fg='green')
            else:
                self.decode_status_label.config(text="Decryption failed", fg='red')
                messagebox.showerror("Error", "Decryption failed! Please check:\n1. The decryption key is correct\n2. The image contains an encrypted message")
                
        except Exception as e:
            self.decode_status_label.config(text="Error occurred", fg='red')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


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
