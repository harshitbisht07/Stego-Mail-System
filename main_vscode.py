"""
VS Code Compatible Enhanced Messaging App
Optimized to work in VS Code terminal
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import tempfile
from datetime import datetime
import sys

# Add error handling for imports
try:
    from steganography import Steganography
    STEGO_AVAILABLE = True
except ImportError as e:
    print(f"Steganography module not available: {e}")
    STEGO_AVAILABLE = False

try:
    from email_sender import EmailSender
    EMAIL_AVAILABLE = True
except ImportError as e:
    print(f"Email module not available: {e}")
    EMAIL_AVAILABLE = False

try:
    from authentication import AuthenticationManager, LoginWindow
    AUTH_AVAILABLE = True
except ImportError as e:
    print(f"Authentication module not available: {e}")
    AUTH_AVAILABLE = False


class VSCodeCompatibleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Secure Messaging - VS Code Compatible")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize modules if available
        self.stego = Steganography() if STEGO_AVAILABLE else None
        self.email_sender = EmailSender() if EMAIL_AVAILABLE else None
        self.auth_manager = AuthenticationManager() if AUTH_AVAILABLE else None
        
        # Variables
        self.selected_image_path = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.app_password_var = tk.StringVar()
        self.is_logged_in = False
        
        # Check for existing session
        if AUTH_AVAILABLE and self.auth_manager.load_session():
            self.is_logged_in = True
            self.create_main_interface()
        else:
            self.create_welcome_interface()
        
    def create_welcome_interface(self):
        """Create welcome interface."""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🔐 Enhanced Secure Messaging", 
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="📊 System Status", padding=10)
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # Check module availability
        modules_status = []
        if STEGO_AVAILABLE:
            modules_status.append("✅ Steganography: Available")
        else:
            modules_status.append("❌ Steganography: Not Available")
            
        if EMAIL_AVAILABLE:
            modules_status.append("✅ Email: Available")
        else:
            modules_status.append("❌ Email: Not Available")
            
        if AUTH_AVAILABLE:
            modules_status.append("✅ Authentication: Available")
        else:
            modules_status.append("❌ Authentication: Not Available")
        
        for status in modules_status:
            tk.Label(status_frame, text=status, bg='#f0f0f0').pack(anchor='w', pady=2)
        
        # Options frame
        options_frame = ttk.LabelFrame(self.root, text="🚀 Available Options", padding=10)
        options_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        if AUTH_AVAILABLE:
            login_btn = ttk.Button(options_frame, text="🔑 Login/Register", command=self.show_login)
            login_btn.pack(pady=10)
        
        if STEGO_AVAILABLE:
            stego_btn = ttk.Button(options_frame, text="🖼️ Steganography Only", command=self.show_steganography)
            stego_btn.pack(pady=10)
        
        simple_btn = ttk.Button(options_frame, text="📱 Simple App", command=self.launch_simple_app)
        simple_btn.pack(pady=10)
        
        # Instructions
        instructions_text = """
Available Applications:

🔑 Login/Register - Full enhanced features with authentication
🖼️ Steganography Only - Basic image encoding/decoding
📱 Simple App - Minimal version that always works

If modules are not available, install dependencies:
pip install -r requirements.txt
        """
        instructions_label = tk.Label(
            options_frame, text=instructions_text, 
            bg='#f0f0f0', fg='gray', font=("Arial", 9), justify='left'
        )
        instructions_label.pack(pady=20)
        
    def show_login(self):
        """Show login interface."""
        if not AUTH_AVAILABLE:
            messagebox.showerror("Error", "Authentication module not available")
            return
            
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create login window
        login_window = LoginWindow(self.root, self.auth_manager, self.on_login_success)
        
    def show_steganography(self):
        """Show steganography-only interface."""
        if not STEGO_AVAILABLE:
            messagebox.showerror("Error", "Steganography module not available")
            return
            
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.create_steganography_interface()
        
    def create_steganography_interface(self):
        """Create steganography-only interface."""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🖼️ Steganography Tool", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Image Selection
        image_frame = ttk.LabelFrame(self.root, text="🖼️ Select Image", padding=10)
        image_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(image_frame, text="Image File:").grid(row=0, column=0, sticky='w', pady=5)
        image_entry = ttk.Entry(image_frame, textvariable=self.selected_image_path, width=40)
        image_entry.grid(row=0, column=1, padx=5, pady=5)
        
        browse_btn = ttk.Button(image_frame, text="Browse", command=self.browse_image)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Image Info
        self.image_info_label = tk.Label(image_frame, text="", fg='blue')
        self.image_info_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Message Input
        message_frame = ttk.LabelFrame(self.root, text="💬 Secret Message", padding=10)
        message_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(message_frame, text="Enter your secret message:").pack(anchor='w')
        self.message_text = scrolledtext.ScrolledText(message_frame, height=8, width=60)
        self.message_text.pack(fill='both', expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        encode_btn = ttk.Button(button_frame, text="🔒 Encode Message", command=self.encode_message)
        encode_btn.pack(side='left', padx=10)
        
        decode_btn = ttk.Button(button_frame, text="🔓 Decode Message", command=self.decode_message)
        decode_btn.pack(side='left', padx=10)
        
        back_btn = ttk.Button(button_frame, text="🔙 Back to Menu", command=self.create_welcome_interface)
        back_btn.pack(side='left', padx=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready to encode/decode messages", fg='green')
        self.status_label.pack(pady=10)
        
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
            
    def show_image_info(self, image_path):
        """Show image information."""
        try:
            from PIL import Image
            image = Image.open(image_path)
            text = f"Size: {image.size[0]}x{image.size[1]} | Mode: {image.mode}"
            self.image_info_label.config(text=text)
        except Exception as e:
            self.image_info_label.config(text=f"Error: {str(e)}")
            
    def encode_message(self):
        """Encode message in image."""
        if not self.selected_image_path.get():
            messagebox.showerror("Error", "Please select an image file")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
            
        try:
            # Create output filename
            input_path = self.selected_image_path.get()
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"{base_name}_encoded.png"
            
            self.status_label.config(text="Encoding message...", fg='orange')
            self.root.update()
            
            success = self.stego.encode_message(input_path, message, output_path)
            
            if success:
                self.status_label.config(text=f"Message encoded successfully! Saved as: {output_path}", fg='green')
                messagebox.showinfo("Success", f"Message encoded successfully!\nSaved as: {output_path}")
            else:
                self.status_label.config(text="Failed to encode message", fg='red')
                messagebox.showerror("Error", "Failed to encode message")
                
        except Exception as e:
            self.status_label.config(text="Error occurred", fg='red')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def decode_message(self):
        """Decode message from image."""
        if not self.selected_image_path.get():
            messagebox.showerror("Error", "Please select an image file")
            return
            
        try:
            self.status_label.config(text="Decoding message...", fg='orange')
            self.root.update()
            
            decoded_message = self.stego.decode_message(self.selected_image_path.get())
            
            if decoded_message:
                self.status_label.config(text="Message decoded successfully!", fg='green')
                
                # Show decoded message in a new window
                decode_window = tk.Toplevel(self.root)
                decode_window.title("Decoded Message")
                decode_window.geometry("400x300")
                
                tk.Label(decode_window, text="Decoded Message:", font=("Arial", 12, "bold")).pack(pady=10)
                
                message_text = scrolledtext.ScrolledText(decode_window, height=10, width=50)
                message_text.pack(padx=20, pady=10, fill='both', expand=True)
                message_text.insert("1.0", decoded_message)
                message_text.config(state='disabled')
                
                close_btn = ttk.Button(decode_window, text="Close", command=decode_window.destroy)
                close_btn.pack(pady=10)
                
            else:
                self.status_label.config(text="No message found or decode failed", fg='red')
                messagebox.showwarning("Warning", "No secret message found in the image")
                
        except Exception as e:
            self.status_label.config(text="Error occurred", fg='red')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def launch_simple_app(self):
        """Launch the simple app."""
        import subprocess
        try:
            subprocess.Popen([sys.executable, "simple_app.py"])
            messagebox.showinfo("Info", "Simple app launched in new window")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch simple app: {e}")
    
    def on_login_success(self):
        """Handle successful login."""
        self.is_logged_in = True
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create main interface after login."""
        # This would be the full enhanced interface
        # For now, show a simple message
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.root, 
            text="🎉 Successfully logged in!\nEnhanced features would be available here.", 
            font=("Arial", 14),
            bg='#f0f0f0'
        ).pack(expand=True)


def main():
    """Main function."""
    print("Starting VS Code Compatible Enhanced App...")
    
    try:
        root = tk.Tk()
        app = VSCodeCompatibleApp(root)
        
        print("Application started successfully!")
        print("GUI should be visible now...")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()