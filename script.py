import smtplib
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart
import os
import sys

def send_mail(workflow_name, repo_name, workflow_run_id):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')  
    receiver_email = os.getenv('RECEIVER_EMAIL')

    if not all([sender_email, sender_password, receiver_email]):
        print("Missing one or more required environment variables.")
        sys.exit(1)

    # email message
    subject = f"Workflow {workflow_name} completed for repo {repo_name}"
    body = (
        f"Hi,\n\nThe workflow **{workflow_name}** just completed for the repo **{repo_name}**.\n"
        f"🔗 View it here: https://github.com/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{workflow_run_id}\n\n"
        f"Cheers,\nGitHub Actions"
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email      
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}") 
        sys.exit(1)


if __name__ == "__main__":
    send_mail(
        os.getenv('WORKFLOW_NAME'),
        os.getenv('REPO_NAME'),
        os.getenv('WORKFLOW_RUN_ID')
    )
