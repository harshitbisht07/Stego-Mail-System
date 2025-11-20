"""
Simplified Image-Based Secure Messaging Application
Optimized for VS Code compatibility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import tempfile
from datetime import datetime
import hashlib
import json

# Simple steganography without external dependencies
class SimpleSteganography:
    def __init__(self):
        self.max_message_length = 500
    
    def encode_message(self, image_path, message, output_path):
        """Simple LSB encoding without encryption for testing."""
        try:
            from PIL import Image
            import numpy as np
            
            # Open image
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            
            # Add delimiter
            message += "###END###"
            
            # Convert to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            
            # Check size
            total_pixels = img_array.shape[0] * img_array.shape[1] * 3
            if len(binary_message) > total_pixels:
                raise ValueError("Image too small for message")
            
            # Encode
            flat_img = img_array.flatten()
            for i, bit in enumerate(binary_message):
                if i < len(flat_img):
                    flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            img_array = flat_img.reshape(img_array.shape)
            encoded_image = Image.fromarray(img_array.astype(np.uint8))
            encoded_image.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"Encoding error: {e}")
            return False
    
    def decode_message(self, image_path):
        """Simple LSB decoding."""
        try:
            from PIL import Image
            import numpy as np
            
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            flat_img = img_array.flatten()
            
            # Extract LSBs
            binary_message = ""
            for pixel in flat_img:
                binary_message += str(pixel & 1)
            
            # Convert to text
            message = ""
            for i in range(0, len(binary_message), 8):
                if i + 8 <= len(binary_message):
                    byte = binary_message[i:i+8]
                    char = chr(int(byte, 2))
                    message += char
                    
                    if message.endswith("###END###"):
                        message = message[:-9]
                        break
            
            return message
            
        except Exception as e:
            print(f"Decoding error: {e}")
            return None


class SimpleMessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Secure Messaging")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize steganography
        self.stego = SimpleSteganography()
        
        # Variables
        self.selected_image_path = tk.StringVar()
        self.recipient_email = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI widgets."""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🔐 Simple Image-Based Secure Messaging", 
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
        
        # Recipient
        recipient_frame = ttk.LabelFrame(self.root, text="📧 Recipient", padding=10)
        recipient_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(recipient_frame, text="Recipient Email:").grid(row=0, column=0, sticky='w', pady=5)
        recipient_entry = ttk.Entry(recipient_frame, textvariable=self.recipient_email, width=40)
        recipient_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        encode_btn = ttk.Button(button_frame, text="🔒 Encode Message", command=self.encode_message)
        encode_btn.pack(side='left', padx=10)
        
        decode_btn = ttk.Button(button_frame, text="🔓 Decode Message", command=self.decode_message)
        decode_btn.pack(side='left', padx=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready to encode/decode messages", fg='green')
        self.status_label.pack(pady=10)
        
        # Instructions
        instructions_text = """
Instructions:
1. Select an image file
2. Type your secret message
3. Click 'Encode Message' to hide message in image
4. Use 'Decode Message' to extract hidden messages
5. Enter recipient email for sending (requires email setup)
        """
        instructions_label = tk.Label(
            self.root, text=instructions_text, 
            bg='#f0f0f0', fg='gray', font=("Arial", 9), justify='left'
        )
        instructions_label.pack(pady=10)
        
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


def main():
    """Main function."""
    print("Starting Simple Secure Messaging App...")
    
    try:
        root = tk.Tk()
        app = SimpleMessagingApp(root)
        
        print("Application started successfully!")
        print("GUI should be visible now...")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







