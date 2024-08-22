The script is configured on Xbuntu to execute on startup and run autonomously.

This Python script is created to monitor for drive mounting, logs data, and alerts via email.
This is triggered upon the drive being mounted. 
The email service Gmail is used, and App password service must be configured to sign in and send emails from the Gmail account. 
I chose Gmail for this purpose with securing the email operations using an app password.

I used Python libraries that would enable functionality of system resources and email alerts. 
The libraries used in formatting and emailing are smtplib and MIMEText, which are necessary to format and send alerts. 
System operation tasks such as checking network settings and managing file operations were handled using the os, time, datetime, socket, and getpass libraries. 
The monitoring function uses the main and while loop, allowing it to maintain the status of the honeypot partition.
Within this loop it checks whether the partition mount status has changed since the last check to prevent unnecessary alerts.
If access is detected the script triggers the function to log access details and send email alerts. When triggered on mount the send email alert function sends an email to a recipient using SMTP protocol.
This is done through Gmail's email service with authentication.
This involves setting up MIME text for the email body, subject, the email address that is sending and the email address that is receiving the email.
Simultaneously, log access function records the incident in a log file.
This gathers essential information such as the current time, user, machine name, and IP address. It formats this information and appends it to a specified log file. 
