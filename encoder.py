import os
from PIL import Image

def encode_message(image_path, secret_message):
    """Encodes a secret message into an image using LSB steganography."""
    try:
        # Open the image
        img = Image.open(image_path, 'r')
        width, height = img.size
        # The image must be a copy to be modified
        encoded_img = img.copy()
        
        # Convert message to binary and add a delimiter to know where the message ends
        binary_message = ''.join([format(ord(i), "08b") for i in secret_message]) + "1111111111111110"
        
        # Check if the image can hold the message
        if len(binary_message) > width * height * 3:
            raise ValueError("Image is too small to hold the secret message.")
            
        # Create a pixel map for modification
        pixels = encoded_img.load()
        data_index = 0
        
        # Iterate over each pixel
        for y in range(height):
            for x in range(width):
                # Get the RGB values of the current pixel
                r, g, b = pixels[x, y]
                
                # Encode bits into each color channel (R, G, B)
                if data_index < len(binary_message):
                    pixels[x, y] = (r & 0b11111110 | int(binary_message[data_index], 2), g, b)
                    data_index += 1
                if data_index < len(binary_message):
                    pixels[x, y] = (r, g & 0b11111110 | int(binary_message[data_index], 2), b)
                    data_index += 1
                if data_index < len(binary_message):
                    pixels[x, y] = (r, g, b & 0b11111110 | int(binary_message[data_index], 2))
                    data_index += 1
                    
        return encoded_img
        
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred during encoding: {e}")
        return None

if __name__ == '__main__':
    cover_image_path = "cover_image.png"  # Replace with your image file
    secret_text = "This is a confidential message for a secure person."
    
    stego_image = encode_message(cover_image_path, secret_text)
    if stego_image:
        stego_image_path = "stego_image.png"
        stego_image.save(stego_image_path)
        print(f"Message successfully encoded and saved to {stego_image_path}")