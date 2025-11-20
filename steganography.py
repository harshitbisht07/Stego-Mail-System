"""
LSB Steganography Module
Handles encoding and decoding of secret messages in images using Least Significant Bit technique.
Includes encryption/decryption with user keys for additional security.
"""

from PIL import Image
import numpy as np
import os
import hashlib
from cryptography.fernet import Fernet
import base64


class Steganography:
    def __init__(self):
        self.max_message_length = 1000  # Maximum characters for safety
    
    def _encrypt_message(self, message, key):
        """Encrypt message using Fernet encryption."""
        try:
            # Create key from user's decryption key
            key_bytes = hashlib.sha256(key.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            fernet = Fernet(fernet_key)
            
            # Encrypt message
            encrypted_message = fernet.encrypt(message.encode())
            return base64.urlsafe_b64encode(encrypted_message).decode()
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return None
    
    def _decrypt_message(self, encrypted_message, key):
        """Decrypt message using Fernet decryption."""
        try:
            # Create key from user's decryption key
            key_bytes = hashlib.sha256(key.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            fernet = Fernet(fernet_key)
            
            # Decrypt message
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_message.encode())
            decrypted_message = fernet.decrypt(encrypted_bytes)
            return decrypted_message.decode()
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return None
    
    def encode_message(self, image_path, message, output_path, encryption_key=None):
        """
        Encode a secret message into an image using LSB steganography.
        
        Args:
            image_path (str): Path to the original image
            message (str): Secret message to hide
            output_path (str): Path to save the encoded image
            encryption_key (str): Optional encryption key for additional security
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Check if message is too long
            if len(message) > self.max_message_length:
                raise ValueError(f"Message too long. Maximum {self.max_message_length} characters allowed.")
            
            # Encrypt message if key provided
            if encryption_key:
                encrypted_message = self._encrypt_message(message, encryption_key)
                if encrypted_message is None:
                    raise ValueError("Failed to encrypt message")
                message = encrypted_message
            
            # Add delimiter to mark end of message
            message += "###END###"
            
            # Convert message to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            
            # Check if image has enough pixels
            total_pixels = img_array.shape[0] * img_array.shape[1] * 3
            if len(binary_message) > total_pixels:
                raise ValueError("Image too small to hide the message.")
            
            # Flatten the image array
            flat_img = img_array.flatten()
            
            # Encode message into LSBs
            for i, bit in enumerate(binary_message):
                if i < len(flat_img):
                    # Clear the LSB and set it to our bit
                    flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            # Reshape back to original shape
            img_array = flat_img.reshape(img_array.shape)
            
            # Save the encoded image
            encoded_image = Image.fromarray(img_array.astype(np.uint8))
            encoded_image.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"Error encoding message: {str(e)}")
            return False
    
    def decode_message(self, image_path, decryption_key=None):
        """
        Decode a secret message from an image using LSB steganography.
        
        Args:
            image_path (str): Path to the encoded image
            decryption_key (str): Optional decryption key for encrypted messages
            
        Returns:
            str: Decoded message or None if failed
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Flatten the image array
            flat_img = img_array.flatten()
            
            # Extract LSBs
            binary_message = ""
            for pixel in flat_img:
                binary_message += str(pixel & 1)
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_message), 8):
                if i + 8 <= len(binary_message):
                    byte = binary_message[i:i+8]
                    char = chr(int(byte, 2))
                    message += char
                    
                    # Check for end delimiter
                    if message.endswith("###END###"):
                        message = message[:-9]  # Remove delimiter
                        break
            
            # Try to decrypt if key provided
            if decryption_key and message:
                decrypted_message = self._decrypt_message(message, decryption_key)
                if decrypted_message is not None:
                    return decrypted_message
                else:
                    # Decryption failed - wrong key or message not encrypted
                    return None
            
            # If no key provided but message exists, return it (might be unencrypted)
            return message
            
        except Exception as e:
            print(f"Error decoding message: {str(e)}")
            return None
    
    def get_image_info(self, image_path):
        """
        Get information about an image file.
        
        Args:
            image_path (str): Path to the image
            
        Returns:
            dict: Image information or None if failed
        """
        try:
            image = Image.open(image_path)
            return {
                'size': image.size,
                'mode': image.mode,
                'format': image.format,
                'file_size': os.path.getsize(image_path)
            }
        except Exception as e:
            print(f"Error getting image info: {str(e)}")
            return None


# Test function
if __name__ == "__main__":
    stego = Steganography()
    
    # Test encoding
    test_message = "This is a secret message!"
    success = stego.encode_message("test_image.jpg", test_message, "encoded_image.jpg")
    
    if success:
        print("Message encoded successfully!")
        
        # Test decoding
        decoded_message = stego.decode_message("encoded_image.jpg")
        if decoded_message:
            print(f"Decoded message: {decoded_message}")
        else:
            print("Failed to decode message")
    else:
        print("Failed to encode message")
