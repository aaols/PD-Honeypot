import smtplib
from email.mime.text import MIMEText
import os
import time
import socket
import getpass
from datetime import datetime

# Configurations
HONEYPOT_DRIVE_PATH = "(Enter Drive Path)"

LOG_PATH = "(Enter drive path for logs eg Desktop/Log.txt)"

RECV_EMAIL = "123@aao.com" # Address email alerts are sent to
SNDR_EMAIL = "422@gmail.com" # Address emails are sent from
SNDR_APP_PASSWORD = "GMAIL password" # Gmail app password for sender

SEND_EMAIL = True
CREATE_LOG = True

# Flag to track whether honeypot is mounted
honeypot_mounted = False

def get_local_ip():
    """Get the primary local IP address of the machine."""
    try:
        # Connect a UDP socket to a public DNS server to determine the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Cloudflares's public DNS server address for the destination
            s.connect(("1.1.1.1", 80))
            local_ip_address = s.getsockname()[0]
        return local_ip_address
    except Exception:
        return "Unable to determine local IP"

def log_access():
    
    # Check if we are allowed to create log entries
    if not CREATE_LOG:
        return
    
    # Gather system information
    current_user = getpass.getuser()
    machine_name = socket.gethostname()
    local_ip_address = get_local_ip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the log entry
    log_entry = f"{timestamp} | User: {current_user} | Machine: {machine_name} | IP: {local_ip_address}\n"

    # Append the log entry to the log file
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)
        
    print("Added log entry.")

def send_email_alert():
    
    # Check if we are allowed to send emails
    if not SEND_EMAIL:
        return
    
    # Email content
    sender = SNDR_EMAIL
    recipient = RECV_EMAIL
    subject = "Security Alert: Honeypot Access"
    body = "The honeypot partition has been accessed."

    # Setup the MIME
    message = MIMEText(body)
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    # Gmail SMTP server information
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use port 465 for SSL

    # Your Gmail account credentials
    gmail_user = sender
    gmail_password = SNDR_APP_PASSWORD  # Use your Gmail App Password

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(gmail_user, gmail_password)
        server.send_message(message)
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def is_mounted(path):
    """Check if the path is mounted."""
    return os.path.ismount(path)

def main():
    global honeypot_mounted
    
    honeypot_path = HONEYPOT_DRIVE_PATH
    print("Monitoring for honeypot partition mount...")
    
    while True:
        if is_mounted(honeypot_path):
            if not honeypot_mounted:
                honeypot_mounted = True
                print("Honeypot partition mounted")
                send_email_alert()
                log_access()
        else:
            honeypot_mounted = False
            print("Honypot partition not mounted")
            time.sleep(1)  # Check periodically if it is mounted

if __name__ == "__main__":
    main()
