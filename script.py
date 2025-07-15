import smtplib
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart
import os
def send_mail(workflow_name,repo_name,workflow_run_id):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')  
    receiver_email = os.getenv('RECEIVER_EMAIL')

    # email message
    subject = f"workflow {workflow_name} failed for repo {repo_name}"
    body = (
        f"Hi, the workflow {workflow_name} failed for the repo {repo_name}. "
        f"Please check the logs for more details.\n"
        f"More Details:\nRun_ID: {workflow_run_id}"
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email      
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)  # Login to the email account
            server.send_message(msg)  # Send the email message
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}") 


send_mail(os.getenv('WORKFLOW_NAME'),
          os.getenv('REPO_NAME'), os.getenv('WORKFLOW_RUN_ID'))

   
