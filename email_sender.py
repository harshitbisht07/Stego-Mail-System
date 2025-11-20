"""
Email Module
Handles sending encoded images via SMTP with Gmail integration.
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def send_encoded_image(self, sender_email, sender_password, recipient_email, 
                          image_path, subject="Secret Image Message", 
                          body="Please find the attached image."):
        """
        Send an encoded image via email.
        
        Args:
            sender_email (str): Sender's email address
            sender_password (str): Sender's app password
            recipient_email (str): Recipient's email address
            image_path (str): Path to the encoded image
            subject (str): Email subject
            body (str): Email body text
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not all([sender_email, sender_password, recipient_email, image_path]):
                raise ValueError("All email parameters are required")
            
            if not os.path.exists(image_path):
                raise ValueError("Image file does not exist")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach the encoded image
            with open(image_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            
            # Add header as key/value pair to attachment part
            filename = os.path.basename(image_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            
            # Attach the part to message
            msg.attach(part)
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Please check your email and app password.")
            return False
        except smtplib.SMTPRecipientsRefused:
            print("Recipient email address is invalid.")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def validate_email(self, email):
        """
        Basic email validation.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def test_connection(self, email, password):
        """
        Test SMTP connection with given credentials.
        
        Args:
            email (str): Email address
            password (str): App password
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(email, password)
            server.quit()
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


# Test function
if __name__ == "__main__":
    sender = EmailSender()
    
    # Test email validation
    test_email = "test@gmail.com"
    print(f"Email validation for {test_email}: {sender.validate_email(test_email)}")
    
    # Note: Actual sending requires real credentials
    print("Email module loaded successfully!")
