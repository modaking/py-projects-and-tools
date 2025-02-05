import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email_card(sender_email, sender_password, recipients, subject, html_file_path, card_image_path=None):
    try:
        # Check if the file exists before attempting to open it
        if not os.path.exists(html_file_path):
            print(f"Error: The file '{html_file_path}' does not exist.")
            return

        # Read the HTML file content
        try:
            with open(html_file_path, 'r') as file:
                html_content = file.read()
        except Exception as ee:
            print(f"Error: Unable to read the file '{html_file_path}'. Details: {ee}")
            return

        # Create the SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to the server
        server.login(sender_email, sender_password)

        for recipient in recipients:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject

            # Attach the HTML content
            msg.attach(MIMEText(html_content, 'html'))

            # Attach the card image if provided
            if card_image_path and os.path.exists(card_image_path):
                with open(card_image_path, 'rb') as img_file:
                    from email.mime.base import MIMEBase
                    from email import encoders

                    mime_base = MIMEBase('application', 'octet-stream')
                    mime_base.set_payload(img_file.read())
                    encoders.encode_base64(mime_base)
                    mime_base.add_header('Content-Disposition',
                                         f'attachment; filename={os.path.basename(card_image_path)}')
                    msg.attach(mime_base)

            # Send the email
            server.sendmail(sender_email, recipient, msg.as_string())

        # Close the SMTP session
        server.quit()
        print(f"Email successfully sent to {recipients}")

    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # User input
    sender_email = input("Enter your email address: ")
    sender_password = input("Enter your email password (or app password): ")
    receivers= input("Enter number of receivers: ")
    rp = []

    try:
        receivers =int(receivers)

        for i in range(receivers):
            recipient_email = input("Enter the recipient's email address: ")
            rp.append(recipient_email)

    except Exception as e:
        print(f"Failed to add recipient emails: {e}")
    subject = "You're Invited!"

    html_file_path = "your_html_file.html"  # File is in the same directory as the script

    # HTML invitation card content
    message_html = input("Enter your html file: ")

    card_image_path = None  # No image needed as the HTML contains the full invitation card

    # Send the email card
    send_email_card(sender_email, sender_password, rp, subject, message_html, card_image_path)

