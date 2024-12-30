import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from email_validator import validate_email, EmailNotValidError
import os
from dotenv import load_dotenv
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Charger les variables d'environnement
load_dotenv()

def send_email(name: str, email: str, message: str):
    # Valider l'adresse email
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=f"Invalid email: {str(e)}")

    # Configurer les informations d'authentification
    gmail_user = os.getenv('GMAIL_USER')
    gmail_pass = os.getenv('GMAIL_PASS')

    if not gmail_user or not gmail_pass:
        raise HTTPException(status_code=500, detail="Email configuration is missing.")

    # Créer le message MIME
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = "alioumbayang99@gmail.com"
    msg['Subject'] = f"Message from {name}"

    # Corps du message
    body = f"From: {email}\n\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Se connecter au serveur SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)

        # Envoyer le message
        server.sendmail(gmail_user, "alioumbayang99@gmail.com", msg.as_string())
        server.close()

        logging.info(f"Email successfully sent to alioumbayang99@gmail.com")

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=500, detail="Authentication failed. Check your credentials.")
    except smtplib.SMTPConnectError:
        raise HTTPException(status_code=500, detail="Failed to connect to the SMTP server.")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
