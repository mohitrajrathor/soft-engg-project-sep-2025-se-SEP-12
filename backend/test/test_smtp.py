"""
Quick SMTP Configuration Test Script

This script helps you verify your SMTP credentials are working
before using them in the application.

Usage:
    python test_smtp.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection and authentication"""
    
    # Get credentials from .env
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('EMAILS_FROM_EMAIL')
    
    print("=" * 60)
    print("SMTP Configuration Test")
    print("=" * 60)
    print(f"Host: {smtp_host}")
    print(f"Port: {smtp_port}")
    print(f"User: {smtp_user}")
    print(f"From: {from_email}")
    print(f"Password: {'*' * len(smtp_password) if smtp_password else 'NOT SET'}")
    print("=" * 60)
    
    # Check if credentials are set
    if not smtp_user or not smtp_password:
        print("\n❌ ERROR: SMTP_USER or SMTP_PASSWORD not set in .env file")
        print("\nPlease update your .env file with:")
        print("  SMTP_USER=your-email@gmail.com")
        print("  SMTP_PASSWORD=your-16-char-app-password")
        return False
    
    try:
        print("\n🔄 Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(0)  # Set to 1 for verbose output
        
        print("🔄 Starting TLS...")
        server.starttls()
        
        print("🔄 Authenticating...")
        server.login(smtp_user, smtp_password)
        
        print("\n✅ SUCCESS! SMTP authentication successful!")
        print("✅ Your credentials are valid and working.")
        
        # Ask if user wants to send a test email
        send_test = input("\nDo you want to send a test email? (yes/no): ").lower()
        
        if send_test == 'yes':
            recipient = input("Enter recipient email address: ")
            
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = recipient
            msg['Subject'] = "AURA - SMTP Test Email"
            
            body = """
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #2563eb;">AURA SMTP Configuration Test</h2>
                    <p>This is a test email to verify your SMTP configuration is working correctly.</p>
                    <p><strong>Status:</strong> ✅ Email service is operational!</p>
                    <p>You can now use the email export feature in AURA.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        <em>This is an automated test message from AURA - Academic Unified Response Assistant</em>
                    </p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            print(f"\n🔄 Sending test email to {recipient}...")
            server.send_message(msg)
            print(f"✅ Test email sent successfully to {recipient}!")
            print("📧 Check your inbox (and spam folder)")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n❌ AUTHENTICATION FAILED!")
        print(f"Error: {e}")
        print("\n🔧 How to fix:")
        print("1. Make sure you're using a Gmail App Password, not your regular password")
        print("2. Enable 2-Factor Authentication on your Google Account")
        print("3. Generate App Password at: https://myaccount.google.com/apppasswords")
        print("4. Copy the 16-character password (remove spaces)")
        print("5. Update SMTP_PASSWORD in your .env file")
        print("\n📖 See SMTP_TROUBLESHOOTING.md for detailed instructions")
        return False
        
    except smtplib.SMTPConnectError as e:
        print("\n❌ CONNECTION FAILED!")
        print(f"Error: {e}")
        print("\n🔧 How to fix:")
        print("1. Check your internet connection")
        print("2. Verify SMTP_HOST and SMTP_PORT in .env")
        print("3. Check if firewall is blocking port 587")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR!")
        print(f"Error: {e}")
        print(f"Error Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  AURA - SMTP Configuration Test")
    print("="*60 + "\n")
    
    success = test_smtp_connection()
    
    print("\n" + "="*60)
    if success:
        print("✅ All tests passed! Your email configuration is ready.")
    else:
        print("❌ Tests failed. Please fix the issues above.")
        print("📖 For detailed help, see: SMTP_TROUBLESHOOTING.md")
    print("="*60 + "\n")
