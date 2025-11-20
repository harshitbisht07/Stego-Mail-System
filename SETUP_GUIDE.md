# Setup Guide for Image-Based Secure Messaging

## Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://python.org)
2. **Gmail Account** - You'll need a Gmail account with App Password enabled

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Enable Gmail App Password
1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Enable 2-Step Verification if not already enabled
4. Go to Security → App passwords
5. Generate a new app password for "Mail"
6. Save this password - you'll need it for the application

### 3. Run the Application
```bash
python main.py
```

## How to Use

### Sending a Secret Message
1. **Login**: Enter your Gmail address and app password
2. **Test Connection**: Click "Test Connection" to verify credentials
3. **Select Image**: Choose any image file (JPG, PNG, BMP, GIF)
4. **Enter Message**: Type your secret message in the text area
5. **Recipient**: Enter the recipient's email address
6. **Send**: Click "Send Secret Message" to encode and email the image

### Decoding a Secret Message
1. **Select Image**: Choose the encoded image file you received
2. **Decode**: Click "Decode Secret Message" to extract the hidden text
3. **View Message**: The decoded message will appear in the text area

## Features

- ✅ **LSB Steganography**: Hides messages in image pixels
- ✅ **Email Integration**: Sends encoded images via SMTP
- ✅ **User-Friendly GUI**: Simple interface with tabs
- ✅ **Image Validation**: Checks image compatibility
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **Security**: Uses app passwords for authentication

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Ensure 2-Step Verification is enabled
   - Use App Password, not your regular password
   - Check email format (must be valid Gmail)

2. **Image Too Small**
   - Use larger images for longer messages
   - Maximum message length: 1000 characters

3. **Connection Issues**
   - Check internet connection
   - Verify SMTP settings (Gmail: smtp.gmail.com:587)

### Testing the System
Run the test script to verify functionality:
```bash
python test_steganography.py
```

## Security Notes

- Messages are hidden using LSB steganography
- Only someone with the decoding tool can extract messages
- Use App Passwords for enhanced security
- Images appear normal to casual observers

## File Structure
```
CRYPT/
├── main.py                 # Main GUI application
├── steganography.py        # LSB steganography module
├── email_sender.py         # Email functionality
├── test_steganography.py   # Test script
├── requirements.txt        # Dependencies
└── README.md              # This file
```
